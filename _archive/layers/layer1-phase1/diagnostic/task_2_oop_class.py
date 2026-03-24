"""
Task 2: OOP Class Implementation

Requirements:
1. Create a class called `BankAccount`
2. Implement `__init__` with parameters: owner (str), balance (float)
3. Implement at least 2 methods:
   - deposit(amount: float) -> bool: Add money, return True if successful
   - withdraw(amount: float) -> bool: Remove money, return False if insufficient funds
4. Implement `__repr__` that returns a useful string representation

Example usage:
>>> account = BankAccount("Alice", 1000.0)
>>> account.deposit(500.0)
True
>>> account.withdraw(200.0)
True
>>> account.withdraw(5000.0)  # Insufficient funds
False
>>> repr(account)
"BankAccount(owner='Alice', balance=1300.0)"

Time: 20 minutes
"""

from typing import Optional


class BankAccount:
    """Bank account with deposit and withdrawal functionality."""

    def __init__(self, owner: str, balance: float):
        """Initialize account with owner and balance."""
        # TODO: Set up instance variables
        pass

    def deposit(self, amount: float) -> bool:
        """Deposit money into account."""
        # TODO: Implement deposit logic
        # Return True if successful, False if amount is invalid
        pass

    def withdraw(self, amount: float) -> bool:
        """Withdraw money from account."""
        # TODO: Implement withdraw logic
        # Return True if successful, False if insufficient funds
        pass

    def __repr__(self) -> str:
        """Return string representation of account."""
        # TODO: Return useful string representation
        pass


# Example usage (for manual testing)
if __name__ == "__main__":
    account = BankAccount("Alice", 1000.0)
    print(f"Initial: {account}")
    print(f"Deposit 500: {account.deposit(500)}")
    print(f"Withdraw 200: {account.withdraw(200)}")
    print(f"Withdraw 5000: {account.withdraw(5000)}")
    print(f"Final: {account}")
