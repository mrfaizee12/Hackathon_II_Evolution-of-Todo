# Quickstart Guide: Phase I Intermediate

**Feature**: 001-phase-i-intermediate
**Date**: 2026-01-01
**Purpose**: Setup and usage guide for Phase I Intermediate features (priority, tags, search, filter, sort)

## Development Setup

### Prerequisites

- Python 3.11+ installed
- Existing Phase I Basic todo application code
- Phase I Intermediate specification and plan approved

### Quick Setup

1. **Create feature branch** (already done):
   ```bash
   git checkout 001-phase-i-intermediate
   ```

2. **Verify existing Phase I Basic code**:
   ```bash
   # Run existing tests to confirm baseline
   pytest tests/ -v
   ```

3. **Review Phase I Intermediate artifacts**:
   ```bash
   # Read the specification
   cat specs/001-phase-i-intermediate/spec.md

   # Read the implementation plan
   cat specs/001-phase-i-intermediate/plan.md

   # Read data model
   cat specs/001-phase-i-intermediate/data-model.md
   ```

### Development Workflow

1. **Extend Task model** (src/models/task.py):
   - Add `priority` field (defaults to Priority.MEDIUM)
   - Add `tags` field (defaults to empty list)
   - Create Priority enum (src/models/enums.py)

2. **Extend TaskService** (src/services/task_service.py):
   - Add `search_tasks(keyword)` method
   - Add `filter_tasks(status, priority, tag)` method
   - Add `sort_tasks(tasks, sort_by)` method
   - Add `update_task_priority(task_id, priority)` method
   - Add `update_task_tags(task_id, tags)` method

3. **Extend CLI layer** (src/cli/):
   - Add input handlers (input_handler.py):
     - `get_priority_choice()`
     - `get_tags_input()`
     - `get_search_keyword()`
     - `get_filter_status()`
     - `get_filter_priority()`
     - `get_filter_tag(service)`
     - `get_sort_choice()`
   - Add menu handlers (menu.py):
     - `update_task_priority(service)`
     - `manage_task_tags(service)`
     - `search_tasks(service)`
     - `filter_tasks(service)`
     - `sort_tasks(service)`
   - Extend output formatter (output_formatter.py):
     - `format_task_list()` to display priority and tags

4. **Add validators** (src/utils/validators.py):
   - `validate_tag(tag)`
   - `validate_tags(tags)`
   - `validate_priority(value)`

5. **Extend tests** (tests/):
   - Add unit tests for Priority enum
   - Add unit tests for search, filter, sort methods
   - Add contract tests (tests/contract/test_cli_operations.py)
   - Extend integration tests (tests/integration/test_todo_app_flows.py)

6. **Run tests**:
   ```bash
   # Run all tests
   pytest tests/ -v

   # Run specific test file
   pytest tests/unit/test_task_model.py -v
   ```

7. **Manual testing**:
   ```bash
   # Run the application
   python src/main.py

   # Test each new feature:
   # - Create task with priority and tags
   # - Update task priority
   # - Manage task tags
   # - Search tasks
   # - Filter tasks
   # - Sort tasks
   ```

## New Feature Usage Examples

### 1. Create Task with Priority and Tags

**Menu Navigation**:
1. Run application: `python src/main.py`
2. Select option 2: "Add a new task"

**User Interaction**:
```
--- Add New Task ---
Enter task title: Review API documentation
Enter task description (press Enter to skip): Check REST endpoints for new feature
Select priority (High/Medium/Low) [High]: High
Enter tags (comma-separated, press Enter to skip): work, urgent, backend

Task added successfully! (ID: 1)
```

**Result**:
- Task created with High priority
- Task has 3 tags: work, urgent, backend
- Task displays with priority and tags in task list

---

### 2. Update Task Priority

**Menu Navigation**:
1. Run application: `python src/main.py`
2. Select option 7: "Update task priority"

**User Interaction**:
```
--- Update Task Priority ---
Enter task ID: 1
Current priority: High
Select new priority (High/Medium/Low): Medium

Task priority updated successfully!
```

**Result**:
- Task ID 1 priority changed from High to Medium
- New priority reflected in task list

---

### 3. Manage Task Tags (Add)

**Menu Navigation**:
1. Run application: `python src/main.py`
2. Select option 8: "Manage task tags"

**User Interaction**:
```
--- Manage Task Tags ---
Enter task ID: 1
Current tags: work, urgent, backend

Action:
1. Add tags
2. Remove tag
3. Replace all tags
Select action: 1

Enter tags to add (comma-separated): important, q4
Tags added successfully! (Tags: work, urgent, backend, important, q4)
```

**Result**:
- Tags added to existing task
- Task now has 5 tags (work, urgent, backend, important, q4)

---

### 4. Manage Task Tags (Remove)

**Menu Navigation**:
1. Run application: `python src/main.py`
2. Select option 8: "Manage task tags"

**User Interaction**:
```
--- Manage Task Tags ---
Enter task ID: 1
Current tags: work, urgent, backend, important, q4

Action:
1. Add tags
2. Remove tag
3. Replace all tags
Select action: 2

Enter tag to remove: urgent
Tag removed successfully! (Tags: work, backend, important, q4)
```

**Result**:
- Tag removed from task
- Task now has 4 tags (work, backend, important, q4)

---

### 5. Search Tasks

**Menu Navigation**:
1. Run application: `python src/main.py`
2. Select option 9: "Search tasks"

**User Interaction**:
```
--- Search Tasks ---
Enter search keyword (press Enter to show all): API

[Search Results: 'API']

  1. Review API documentation [High]
      Check REST endpoints for new feature
      Tags: work, backend, important, q4
      Status: Incomplete
------------------------------

  3. Implement authentication [Medium]
      Add login/logout to application
      Tags: auth, security
      Status: Incomplete
------------------------------

2 tasks found matching 'API'
```

**Result**:
- Displays tasks containing "API" in title OR description
- Case-insensitive search (matches "API", "api", "Api")
- Shows count of matching tasks

---

### 6. Filter Tasks

**Menu Navigation**:
1. Run application: `python src/main.py`
2. Select option 10: "Filter tasks"

**User Interaction**:
```
--- Filter Tasks ---
Filter by status:
1. All
2. Complete
3. Incomplete
Select status filter: 3

Filter by priority:
1. All
2. High
3. Medium
4. Low
Select priority filter: 2

Filter by tag (available: work, backend, important, q4, auth, security, urgent):
1. All tags
2. work
3. backend
4. important
5. q4
6. auth
7. security
8. urgent
Select tag filter: 1

[Filtered: Incomplete, High priority, All tags]

  1. Review API documentation [High]
      Check REST endpoints for new feature
      Tags: work, backend, important, q4
      Status: Incomplete
------------------------------

1 task matches current filters.
```

**Result**:
- Shows tasks matching all filters (AND logic)
- Displays active filters in header
- Shows available tags for tag filter selection
- Empty filters return all tasks

---

### 7. Sort Tasks

**Menu Navigation**:
1. Run application: `python src/main.py`
2. Select option 11: "Sort tasks"

**User Interaction**:
```
--- Sort Tasks ---
Sort by:
1. Title (A-Z)
2. Title (Z-A)
3. Priority (High to Low)
4. Priority (Low to High)
Select sort order: 1

[Sorted by: Title (A-Z)]

  3. Add unit tests [Low]
      Write tests for new features
      Tags: testing, quality
      Status: Incomplete
------------------------------

  1. Review API documentation [High]
      Check REST endpoints for new feature
      Tags: work, backend, important, q4
      Status: Incomplete
------------------------------

  2. Fix authentication bug [Medium]
      Resolve login issue reported by user
      Tags: bug, auth
      Status: Incomplete
------------------------------

3 tasks sorted by title (A-Z).
```

**Result**:
- Tasks sorted alphabetically (case-insensitive)
- Sort order shown in header
- Stable sort maintains order for identical titles

---

### 8. Combine Search, Filter, and Sort

**Menu Navigation**:
1. Search for "test" (option 9)
2. Filter results by "Incomplete" and "High" priority (option 10)
3. Sort filtered results by "Priority (High to Low)" (option 11)

**User Interaction**:
```
--- Search Tasks ---
Enter search keyword (press Enter to show all): test
2 tasks found matching 'test'

--- Filter Tasks ---
[Current: Search Results]
Filter by status:
1. All
2. Complete
3. Incomplete
Select status filter: 3

Filter by priority:
1. All
2. High
3. Medium
4. Low
Select priority filter: 2

[Filtered: Search Results → Incomplete, High priority]

  5. Write integration tests [High]
      Test search, filter, sort features together
      Tags: testing, integration
      Status: Incomplete
------------------------------

1 task matches current filters.

--- Sort Tasks ---
[Current: Filtered Results]
Sort by:
1. Title (A-Z)
2. Title (Z-A)
3. Priority (High to Low)
4. Priority (Low to High)
Select sort order: 3

[Sorted by: Priority (High to Low), Filtered: Search Results → Incomplete, High priority]

  5. Write integration tests [High]
      Test search, filter, sort features together
      Tags: testing, integration
      Status: Incomplete
------------------------------

1 task displayed.
```

**Result**:
- Operations apply sequentially (search → filter → sort)
- Each operation shows current state in header
- Final result is 1 task (matching search, filters, and sorted)

---

## Error Handling Examples

### Invalid Priority

**User Interaction**:
```
Select priority (High/Medium/Low): urgent
Invalid priority. Please choose High, Medium, or Low.
Select priority (High/Medium/Low): High
```

**Result**:
- Error message displayed
- User reprompted for valid input
- Only valid priorities (High, Medium, Low) accepted

---

### Tag Too Long

**User Interaction**:
```
Enter tags to add (comma-separated): this-tag-is-way-too-long-and-exceeds-fifty-characters-limit
Tag 'this-tag-is-way-too-long...' exceeds 50 character limit.
Enter tags to add (comma-separated): short-tag
Tags added successfully!
```

**Result**:
- Validation error displayed with clear message
- User reprompted for valid input
- Tag length enforced at 50 characters max

---

### Too Many Tags

**User Interaction**:
```
Enter tags (add): tag1,tag2,tag3,tag4,tag5,tag6,tag7,tag8,tag9,tag10,tag11
Cannot add more than 10 tags to a task.
Enter tags to add): tag1,tag2,tag3,tag4,tag5,tag6,tag7,tag8,tag9,tag10
Tags added successfully!
```

**Result**:
- Validation error displayed
- Maximum 10 tags enforced
- User reprompted for valid input

---

### Empty Search Results

**User Interaction**:
```
--- Search Tasks ---
Enter search keyword: nonexistent
No tasks found matching 'nonexistent'.
Press Enter to continue...
```

**Result**:
- Clear "no results" message displayed
- User can press Enter to return to main menu
- No error or crash on empty results

---

### Empty Filter Results

**User Interaction**:
```
--- Filter Tasks ---
Filter by status: 3 (Incomplete)
Filter by priority: 3 (Low)
Filter by tag: urgent

No tasks match current filters.
Press Enter to continue...
```

**Result**:
- Clear "no tasks match current filters" message displayed
- User can adjust filters or return to main menu
- All filters respected (AND logic)

---

## Testing Checklist

### Manual Testing

Before submitting implementation for review, verify:

**Basic Features (Unchanged)**:
- [ ] Can create task without priority/tags (Basic Level)
- [ ] Can view all tasks (Basic Level)
- [ ] Can update task title/description (Basic Level)
- [ ] Can delete task (Basic Level)
- [ ] Can mark task complete/incomplete (Basic Level)

**Priority Features**:
- [ ] Can create task with High priority
- [ ] Can create task with Medium priority (default)
- [ ] Can create task with Low priority
- [ ] Can update task priority
- [ ] Priority displays in task list
- [ ] Invalid priority rejected with error message

**Tag Features**:
- [ ] Can create task with tags (comma-separated)
- [ ] Can create task with no tags (optional)
- [ ] Can add tags to existing task
- [ ] Can remove tag from existing task
- [ ] Can replace all tags on existing task
- [ ] Tags display in task detail view
- [ ] Tag too long (>50 chars) rejected
- [ ] Too many tags (>10) rejected
- [ ] Special characters in tags preserved

**Search Features**:
- [ ] Can search tasks by keyword in title
- [ ] Can search tasks by keyword in description
- [ ] Search is case-insensitive
- [ ] Empty keyword returns all tasks
- [ ] Empty search results show message
- [ ] Search matches title OR description (OR logic)

**Filter Features**:
- [ ] Can filter by completion status (Complete/Incomplete/All)
- [ ] Can filter by priority (High/Medium/Low/All)
- [ ] Can filter by tag (from available tags)
- [ ] Can combine filters (status + priority + tag)
- [ ] Filters use AND logic
- [ ] Empty filter results show message
- [ ] Active filters displayed
- [ ] Can clear filters to return to all tasks

**Sort Features**:
- [ ] Can sort by title ascending (A-Z)
- [ ] Can sort by title descending (Z-A)
- [ ] Title sort is case-insensitive
- [ ] Can sort by priority (High to Low)
- [ ] Can sort by priority (Low to High)
- [ ] Sort is stable (preserves order for equal keys)
- [ ] Sort applies to filtered results
- [ ] Can clear sort to return to default order

**Backward Compatibility**:
- [ ] Tasks created before feature work (default to Medium, empty tags)
- [ ] Existing Phase I Basic workflows unchanged
- [ ] No breaking changes to existing tests

**Edge Cases**:
- [ ] Duplicate tags handled (ignored or removed)
- [ ] Empty task list shows clear message
- [ ] All tasks deleted from filtered view handled
- [ ] Special characters in search work correctly
- [ ] Whitespace-only search returns all tasks

---

## Common Issues & Solutions

### Issue: Tasks not showing new priority/tags

**Cause**: Task created before Phase I Intermediate implementation

**Solution**: Tasks automatically get default values (Medium priority, empty tags) - no manual migration needed

### Issue: Sort order unexpected

**Cause**: Sort applied to wrong view (e.g., searching then sorting entire list)

**Solution**: Sort applies to current view (filtered results if filters active, search results if search active)

### Issue: Tag filter shows no tags

**Cause**: No tasks have tags yet, or filter menu not refreshed

**Solution**: Create tasks with tags first, then filter menu will show available tags

### Issue: Cannot clear specific filter

**Cause**: Clearing one filter not implemented (must clear all)

**Solution**: Use "All" option to clear that filter type (e.g., "All" for status filter)

---

## Next Steps

After completing Phase I Intermediate implementation:

1. **Run all tests**: `pytest tests/ -v`
2. **Verify backward compatibility**: Ensure existing Basic Level features work unchanged
3. **Manual testing**: Walk through all usage examples above
4. **Commit changes**: `git add . && git commit -m "feat: implement Phase I Intermediate task organization features"`
5. **Ready for**: Code review and merge to main branch

---

## Additional Resources

**Specification**: [spec.md](./spec.md)
**Implementation Plan**: [plan.md](./plan.md)
**Data Model**: [data-model.md](./data-model.md)
**CLI Contracts**: [contracts/cli-operations.yaml](./contracts/cli-operations.yaml)
**Research**: [research.md](./research.md)

---

## Summary

**Quickstart provided** for:
- ✅ Development setup
- ✅ New feature usage examples (8 workflows)
- ✅ Error handling examples
- ✅ Testing checklist (45+ test cases)
- ✅ Common issues and solutions
- ✅ Next steps for implementation

**Ready for**: Implementation with comprehensive usage guide
