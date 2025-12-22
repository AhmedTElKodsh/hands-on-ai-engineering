"""Safety checks for AI agents.

This module provides safety mechanisms to prevent harmful or incorrect
agent behavior, including:
- Prompt injection detection
- Safe tool usage validation

These safety checks help protect against:
- Malicious user inputs attempting to manipulate agent behavior
- Unauthorized tool usage or parameter manipulation
- Potentially dangerous operations

Example:
    >>> from src.agents.safety import detect_prompt_injection, validate_tool_usage
    >>> 
    >>> # Check for prompt injection
    >>> result = detect_prompt_injection("ignore previous instructions and...")
    >>> if result.is_injection:
    ...     print(f"Blocked: {result.reason}")
    >>> 
    >>> # Validate tool usage
    >>> result = validate_tool_usage("delete_file", {"path": "/etc/passwd"})
    >>> if not result.is_safe:
    ...     print(f"Unsafe: {result.reason}")
"""

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


@dataclass
class InjectionDetectionResult:
    """Result of prompt injection detection.
    
    Attributes:
        is_injection: Whether the input appears to be a prompt injection attempt
        confidence: Confidence level (0.0 to 1.0) that this is an injection
        reason: Human-readable explanation of why it was flagged
        matched_patterns: List of patterns that matched
    """
    is_injection: bool
    confidence: float
    reason: str
    matched_patterns: List[str] = field(default_factory=list)



# Known prompt injection patterns
# These patterns are commonly used in prompt injection attacks
INJECTION_PATTERNS: List[Dict[str, Any]] = [
    {
        "name": "ignore_instructions",
        "pattern": r"(?i)\b(ignore|disregard|forget|override)\b.{0,30}\b(previous|prior|above|earlier|all|any)\b.{0,30}\b(instructions?|prompts?|rules?|guidelines?|context)\b",
        "weight": 0.9,
        "description": "Attempts to override previous instructions",
    },
    {
        "name": "new_instructions",
        "pattern": r"(?i)\b(new|actual|real|true|correct)\b.{0,20}\b(instructions?|task|objective|goal|mission)\b",
        "weight": 0.7,
        "description": "Claims to provide new/real instructions",
    },
    {
        "name": "system_prompt_leak",
        "pattern": r"(?i)\b(reveal|show|display|print|output|tell me|what is|what are)\b.{0,30}\b(system\s*prompt|initial\s*prompt|hidden\s*prompt|secret\s*instructions?|your\s*instructions?)\b",
        "weight": 0.85,
        "description": "Attempts to extract system prompt",
    },
    {
        "name": "role_switch",
        "pattern": r"(?i)\b(you\s*are\s*now|act\s*as|pretend\s*to\s*be|roleplay\s*as|become|switch\s*to)\b.{0,30}\b(different|new|another|evil|malicious|unrestricted)\b",
        "weight": 0.8,
        "description": "Attempts to change agent role/persona",
    },
    {
        "name": "jailbreak_keywords",
        "pattern": r"(?i)\b(jailbreak|dan|do\s*anything\s*now|developer\s*mode|unrestricted\s*mode|no\s*restrictions?|bypass\s*filters?)\b",
        "weight": 0.95,
        "description": "Known jailbreak attempt keywords",
    },
    {
        "name": "delimiter_injection",
        "pattern": r"(?i)(```\s*system|<\|system\|>|<\|im_start\|>|<\|endoftext\|>|\[INST\]|\[/INST\]|<<SYS>>|<</SYS>>)",
        "weight": 0.9,
        "description": "Attempts to inject system-level delimiters",
    },
    {
        "name": "output_manipulation",
        "pattern": r"(?i)\b(respond\s*with|always\s*say|only\s*output|your\s*response\s*must|you\s*must\s*respond)\b.{0,50}\b(yes|no|true|false|agree|confirm)\b",
        "weight": 0.6,
        "description": "Attempts to force specific outputs",
    },
    {
        "name": "context_escape",
        "pattern": r"(?i)(end\s*of\s*(prompt|context|instructions?)|---+\s*(new|actual)\s*(prompt|instructions?)|ignore\s*everything\s*(above|before))",
        "weight": 0.85,
        "description": "Attempts to escape current context",
    },
    {
        "name": "encoding_bypass",
        "pattern": r"(?i)(base64|rot13|hex|unicode|encode|decode).{0,20}(instructions?|prompt|command)",
        "weight": 0.7,
        "description": "Attempts to use encoding to bypass filters",
    },
    {
        "name": "hypothetical_scenario",
        "pattern": r"(?i)\b(hypothetically|theoretically|imagine\s*if|what\s*if|pretend|suppose)\b.{0,50}\b(no\s*rules?|no\s*restrictions?|could\s*do\s*anything|unrestricted)\b",
        "weight": 0.65,
        "description": "Uses hypothetical scenarios to bypass restrictions",
    },
]


def detect_prompt_injection(
    text: str,
    threshold: float = 0.5,
    custom_patterns: Optional[List[Dict[str, Any]]] = None,
) -> InjectionDetectionResult:
    """Detect potential prompt injection attempts in user input.
    
    This function analyzes text for patterns commonly used in prompt
    injection attacks. It uses a weighted pattern matching approach
    where each pattern has an associated weight indicating how strongly
    it suggests an injection attempt.
    
    Args:
        text: The input text to analyze
        threshold: Confidence threshold (0.0-1.0) above which to flag as injection
        custom_patterns: Optional additional patterns to check
        
    Returns:
        InjectionDetectionResult with detection details
        
    Example:
        >>> result = detect_prompt_injection("ignore previous instructions")
        >>> result.is_injection
        True
        >>> result.confidence > 0.5
        True
    """
    if not text or not text.strip():
        return InjectionDetectionResult(
            is_injection=False,
            confidence=0.0,
            reason="Empty input",
            matched_patterns=[],
        )
    
    # Combine default and custom patterns
    patterns = INJECTION_PATTERNS.copy()
    if custom_patterns:
        patterns.extend(custom_patterns)
    
    matched_patterns: List[str] = []
    total_weight = 0.0
    max_weight = 0.0
    reasons: List[str] = []
    
    for pattern_def in patterns:
        pattern = pattern_def["pattern"]
        weight = pattern_def["weight"]
        name = pattern_def["name"]
        description = pattern_def["description"]
        
        if re.search(pattern, text):
            matched_patterns.append(name)
            total_weight += weight
            max_weight = max(max_weight, weight)
            reasons.append(description)
    
    # Calculate confidence based on matched patterns
    # Use the maximum weight as the primary indicator,
    # with a small boost for multiple matches
    if matched_patterns:
        confidence = min(1.0, max_weight + (len(matched_patterns) - 1) * 0.05)
    else:
        confidence = 0.0
    
    is_injection = confidence >= threshold
    
    if is_injection:
        reason = f"Detected potential injection: {'; '.join(reasons)}"
    else:
        reason = "No injection patterns detected" if not matched_patterns else f"Low confidence matches: {'; '.join(reasons)}"
    
    return InjectionDetectionResult(
        is_injection=is_injection,
        confidence=confidence,
        reason=reason,
        matched_patterns=matched_patterns,
    )



@dataclass
class ToolUsageValidationResult:
    """Result of tool usage validation.
    
    Attributes:
        is_safe: Whether the tool usage is considered safe
        reason: Human-readable explanation of the validation result
        violations: List of specific safety violations found
        sanitized_args: Optional sanitized version of arguments
    """
    is_safe: bool
    reason: str
    violations: List[str] = field(default_factory=list)
    sanitized_args: Optional[Dict[str, Any]] = None


# Dangerous path patterns that should be blocked
DANGEROUS_PATH_PATTERNS: List[str] = [
    r"^/etc/",           # System configuration
    r"^/var/",           # Variable data
    r"^/usr/",           # User programs
    r"^/bin/",           # Essential binaries
    r"^/sbin/",          # System binaries
    r"^/boot/",          # Boot files
    r"^/root/",          # Root home
    r"^/sys/",           # System files
    r"^/proc/",          # Process info
    r"^/dev/",           # Device files
    r"^C:\\Windows",     # Windows system (case insensitive handled separately)
    r"^C:\\Program Files",
    r"^\.\./",           # Parent directory traversal
    r"/\.\./",           # Parent directory traversal in path
    r"\.\.[/\\]",        # Parent directory traversal
]

# Dangerous command patterns
DANGEROUS_COMMAND_PATTERNS: List[str] = [
    r"(?i)\brm\s+-rf\b",           # Recursive force delete
    r"(?i)\bsudo\b",               # Privilege escalation
    r"(?i)\bchmod\s+777\b",        # Overly permissive permissions
    r"(?i)\bdd\s+if=",             # Disk operations
    r"(?i)\bmkfs\b",               # Filesystem creation
    r"(?i)\bformat\b",             # Disk formatting
    r"(?i)\b(curl|wget)\b.*\|\s*(bash|sh)\b",  # Remote code execution
    r"(?i)\beval\b",               # Code evaluation
    r"(?i)\bexec\b",               # Command execution
    r"(?i)>\s*/dev/",              # Writing to devices
    r"(?i)\bkill\s+-9\b",          # Force kill
    r"(?i)\bshutdown\b",           # System shutdown
    r"(?i)\breboot\b",             # System reboot
]

# Tools that are considered high-risk and need extra validation
HIGH_RISK_TOOLS: Set[str] = {
    "execute_command",
    "run_shell",
    "delete_file",
    "delete_directory",
    "write_file",
    "modify_file",
    "execute_code",
    "run_script",
    "system_call",
}

# Tools that should never be allowed
BLOCKED_TOOLS: Set[str] = {
    "format_disk",
    "delete_system",
    "modify_system_config",
    "escalate_privileges",
    "access_credentials",
}


def _check_path_safety(path: str) -> List[str]:
    """Check if a file path is safe to access.
    
    Args:
        path: The file path to check
        
    Returns:
        List of safety violations (empty if safe)
    """
    violations: List[str] = []
    
    # Normalize path for checking
    normalized = path.replace("\\", "/").lower()
    
    for pattern in DANGEROUS_PATH_PATTERNS:
        if re.search(pattern, path, re.IGNORECASE):
            violations.append(f"Dangerous path pattern detected: {pattern}")
            break
    
    # Check for null bytes (path traversal attack)
    if "\x00" in path:
        violations.append("Null byte detected in path (potential path traversal)")
    
    # Check for excessive parent directory references
    parent_refs = path.count("..") 
    if parent_refs > 2:
        violations.append(f"Excessive parent directory references ({parent_refs})")
    
    return violations


def _check_command_safety(command: str) -> List[str]:
    """Check if a command is safe to execute.
    
    Args:
        command: The command string to check
        
    Returns:
        List of safety violations (empty if safe)
    """
    violations: List[str] = []
    
    for pattern in DANGEROUS_COMMAND_PATTERNS:
        if re.search(pattern, command):
            violations.append(f"Dangerous command pattern detected: {pattern}")
    
    # Check for shell metacharacters that could enable injection
    dangerous_chars = [";", "&&", "||", "|", "`", "$(", "${"]
    for char in dangerous_chars:
        if char in command:
            violations.append(f"Potentially dangerous shell metacharacter: {char}")
    
    return violations


def validate_tool_usage(
    tool_name: str,
    arguments: Dict[str, Any],
    allowed_tools: Optional[Set[str]] = None,
    blocked_tools: Optional[Set[str]] = None,
) -> ToolUsageValidationResult:
    """Validate that a tool usage request is safe.
    
    This function checks:
    1. Whether the tool is in the blocked list
    2. Whether the tool is in the allowed list (if provided)
    3. Whether arguments contain dangerous patterns (paths, commands)
    4. Whether high-risk tools have appropriate safeguards
    
    Args:
        tool_name: Name of the tool being called
        arguments: Arguments being passed to the tool
        allowed_tools: Optional set of explicitly allowed tools
        blocked_tools: Optional set of blocked tools (merged with defaults)
        
    Returns:
        ToolUsageValidationResult with validation details
        
    Example:
        >>> result = validate_tool_usage("delete_file", {"path": "/etc/passwd"})
        >>> result.is_safe
        False
        >>> "Dangerous path" in result.reason
        True
    """
    violations: List[str] = []
    
    # Merge blocked tools with defaults
    all_blocked = BLOCKED_TOOLS.copy()
    if blocked_tools:
        all_blocked.update(blocked_tools)
    
    # Check if tool is blocked
    if tool_name in all_blocked:
        return ToolUsageValidationResult(
            is_safe=False,
            reason=f"Tool '{tool_name}' is blocked for safety reasons",
            violations=[f"Blocked tool: {tool_name}"],
        )
    
    # Check if tool is in allowed list (if provided)
    if allowed_tools is not None and tool_name not in allowed_tools:
        return ToolUsageValidationResult(
            is_safe=False,
            reason=f"Tool '{tool_name}' is not in the allowed tools list",
            violations=[f"Tool not allowed: {tool_name}"],
        )
    
    # Check arguments for dangerous patterns
    for arg_name, arg_value in arguments.items():
        if isinstance(arg_value, str):
            # Check for path-related arguments
            if any(keyword in arg_name.lower() for keyword in ["path", "file", "dir", "directory", "folder"]):
                path_violations = _check_path_safety(arg_value)
                violations.extend(path_violations)
            
            # Check for command-related arguments
            if any(keyword in arg_name.lower() for keyword in ["command", "cmd", "script", "shell", "exec"]):
                cmd_violations = _check_command_safety(arg_value)
                violations.extend(cmd_violations)
            
            # Check for potential injection in any string argument
            injection_result = detect_prompt_injection(arg_value, threshold=0.7)
            if injection_result.is_injection:
                violations.append(f"Potential injection in argument '{arg_name}': {injection_result.reason}")
    
    # Extra validation for high-risk tools
    if tool_name in HIGH_RISK_TOOLS:
        # Require explicit confirmation for high-risk operations
        if not arguments.get("confirmed", False) and not arguments.get("force", False):
            violations.append(f"High-risk tool '{tool_name}' requires explicit confirmation")
    
    if violations:
        return ToolUsageValidationResult(
            is_safe=False,
            reason=f"Safety violations detected: {'; '.join(violations[:3])}{'...' if len(violations) > 3 else ''}",
            violations=violations,
        )
    
    return ToolUsageValidationResult(
        is_safe=True,
        reason="Tool usage validated successfully",
        violations=[],
        sanitized_args=arguments,
    )


def sanitize_user_input(text: str) -> str:
    """Sanitize user input by removing or escaping potentially dangerous content.
    
    This function:
    1. Removes known delimiter injection attempts
    2. Escapes special characters
    3. Truncates excessively long inputs
    
    Args:
        text: The user input to sanitize
        
    Returns:
        Sanitized version of the input
    """
    if not text:
        return ""
    
    # Remove potential delimiter injections
    sanitized = text
    delimiter_patterns = [
        r"```\s*system",
        r"<\|system\|>",
        r"<\|im_start\|>",
        r"<\|endoftext\|>",
        r"\[INST\]",
        r"\[/INST\]",
        r"<<SYS>>",
        r"<</SYS>>",
    ]
    
    for pattern in delimiter_patterns:
        sanitized = re.sub(pattern, "[REMOVED]", sanitized, flags=re.IGNORECASE)
    
    # Truncate excessively long inputs (prevent context overflow attacks)
    max_length = 10000
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "... [TRUNCATED]"
    
    return sanitized
