# Task 12: Student Validation Testing - Quick Reference Card

**Status**: ✅ Ready for Execution
**Type**: Manual Testing Gate
**Duration**: 1-2 weeks
**Critical**: Yes - blocks scale phase

---

## 🎯 Goal

Validate scaffolded pilot chapters with 2-3 real students to achieve **80%+ completion rate**.

---

## 📋 Quick Checklist

### Pre-Testing

- [ ] Recruit 2-3 testers (intermediate Python, unfamiliar with curriculum)
- [ ] Verify scaffolded chapters exist (`_bmad-output/pilot/scaffolded/`)
- [ ] Prepare testing package (chapters + survey + instructions)
- [ ] Schedule orientation session (30 min)

### Testing (Week 1)

- [ ] Conduct orientation (explain scaffolding, protocol, Q&A)
- [ ] Testers work independently (7-10 hours)
- [ ] Check in every 2-3 days (technical support only, no hints!)
- [ ] Collect feedback surveys and code

### Analysis (Week 2)

- [ ] Calculate completion rates (target: ≥80%)
- [ ] Analyze feedback themes
- [ ] Review submitted code
- [ ] Generate validation report
- [ ] Make gate decision

---

## 📚 Document Guide

| Need                | Document                              | Location      |
| ------------------- | ------------------------------------- | ------------- |
| **Overview**        | TASK-12-README.md                     | Start here    |
| **Step-by-step**    | TESTING-COORDINATOR-CHECKLIST.md      | Follow this   |
| **Detailed guide**  | STUDENT-VALIDATION-GUIDE.md           | Reference     |
| **Tester survey**   | STUDENT-FEEDBACK-SURVEY.md            | Distribute    |
| **Report template** | STUDENT-VALIDATION-REPORT-TEMPLATE.md | After testing |

All in: `_bmad-output/pilot/`

---

## 🎓 Pilot Chapters

1. **Chapter 06A**: Decorators & Context Managers (TIER_1, 3-4 hours)
2. **Chapter 07**: Your First LLM Call (TIER_2, 2-3 hours)
3. **Chapter 17**: Your First RAG System (TIER_2, 2-3 hours)

**Total**: 7-10 hours per tester

---

## ✅ Success Criteria

**Primary**: 80%+ completion rate across all 3 chapters

**Secondary**:

- Time within expected ranges
- Specific, actionable feedback
- Correct implementations

---

## 🚦 Gate Decision

| Completion Rate | Decision       | Next Step                 |
| --------------- | -------------- | ------------------------- |
| ≥80%            | ✅ PASS        | Task 13 (Iteration)       |
| 75-79%          | ⚠️ CONDITIONAL | Discuss with stakeholders |
| <75%            | ❌ FAIL        | Major improvements        |

---

## 👥 Roles

**Coordinator** (10-15 hours over 2 weeks):

- Recruit testers
- Prepare materials
- Conduct orientation
- Monitor progress
- Analyze results
- Make gate decision

**Testers** (7-10 hours over 1 week):

- Complete 3 chapters
- Track time and progress
- Complete feedback survey
- Submit code

**Compensation**: $100-150 per tester

---

## 📊 Data to Collect

1. **Completion rates** (per chapter, per tester, overall)
2. **Time spent** (per chapter, per exercise)
3. **Stuck points** (which exercises, why)
4. **Feedback** (missing hints, unclear hints, what worked)
5. **Code** (implementations for review)

---

## ⚠️ Critical Rules

**Coordinators**:

- ✅ Provide technical support (environment setup)
- ❌ Don't provide hints or solutions

**Testers**:

- ✅ Use hints in chapters + official docs
- ❌ Don't search for external solutions
- ❌ Don't look at original chapters

---

## 🔧 Common Issues

| Issue                          | Solution                                                         |
| ------------------------------ | ---------------------------------------------------------------- |
| Can't find scaffolded chapters | Check `_bmad-output/pilot/scaffolded/` or run Task 10 conversion |
| Testers stuck immediately      | Walk through one example, verify they read educational content   |
| Low completion rates           | Analyze stuck points, identify missing hints, plan improvements  |
| Vague feedback                 | Ask follow-up questions, review code, use structured survey      |

---

## 📞 Quick Contact

**Coordinator**: ********\_********
**Email**: ********\_********
**Slack/Discord**: ********\_********

---

## 🚀 Next Steps After Pass

1. **Task 13**: Iteration based on feedback
   - Update templates
   - Add missing hints
   - Re-convert pilot chapters
   - Re-test

2. **Task 14**: Pilot gate validation
   - Verify improvements
   - Measure improvement
   - Approve scale phase

3. **Scale Phase**: Convert 48+ chapters

---

## 📝 Quick Notes Space

**Tester 1**: ********\_******** (contact: ********\_********)
**Tester 2**: ********\_******** (contact: ********\_********)
**Tester 3**: ********\_******** (contact: ********\_********)

**Orientation Date**: ********\_********
**Testing Start**: ********\_********
**Testing End**: ********\_********
**Analysis Complete**: ********\_********

**Completion Rate**: **\_**%
**Gate Decision**: ✅ PASS / ⚠️ CONDITIONAL / ❌ FAIL

---

**Print this card and keep it handy during testing!**

**Version**: 1.0 | **Date**: January 23, 2026
