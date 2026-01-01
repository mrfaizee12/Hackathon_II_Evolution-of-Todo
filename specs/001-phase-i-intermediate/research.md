# Research & Decisions: Phase I Intermediate

**Feature**: 001-phase-i-intermediate
**Date**: 2026-01-01
**Purpose**: Document research outcomes and technical decisions for Phase I Intermediate implementation

## Research Summary

Since the Phase I Intermediate specification is complete and follows existing Phase I Basic patterns, no external research was required. All technical decisions use Python standard library features that match the current implementation approach.

## Research Tasks (All Completed)

### 1. Task Priority Data Structure

**Decision**: Use Python `enum.Enum` for Priority levels (High, Medium, Low)

**Rationale**:
- Type-safe alternative to string literals
- Clear, self-documenting code (Priority.HIGH vs "High")
- Built-in validation (invalid values rejected at runtime)
- Easy to extend (add new priorities in future phases without breaking existing code)
- Matches existing Phase I Basic code style (no external dependencies)

**Alternatives Considered**:
1. **String literals** ("High", "Medium", "Low")
   - Rejected: No compile-time type safety, typos possible
2. **Integer constants** (HIGH=3, MEDIUM=2, LOW=1)
   - Rejected: Less readable, requires documentation for values
3. **Integer Enum** (IntEnum)
   - Rejected: No sorting advantage, string values needed for display

**Final Decision**: Python `enum.Enum` with string values for user-friendly display

---

### 2. Tags Data Structure

**Decision**: Use `list[str]` stored in Task dataclass with `field(default_factory=list)`

**Rationale**:
- Zero or more tags naturally represented as list
- No need for specialized Tag model (just string labels)
- Easy to iterate, filter, and display
- No external dependencies (built-in type)
- Matches Python typing best practices (list[str] syntax)

**Alternatives Considered**:
1. **Custom Tag model** (dataclass with id, label, created_at)
   - Rejected: Over-engineering, tags are just labels, no entity semantics
2. **Set[str]** for automatic deduplication
   - Rejected: Preserves insertion order is important for user expectations
   - Rejected: Duplicate handling is edge case, not core requirement
3. **String with delimiter** (e.g., "work,home,personal")
   - Rejected: Harder to parse, validate, and display

**Final Decision**: `list[str] with manual duplicate removal in edge cases

---

### 3. In-Memory Search Algorithm

**Decision**: Linear scan with list comprehension and case-insensitive comparison

**Rationale**:
- Simplicity: O(n) complexity acceptable for ≤100 tasks (Phase I scope)
- No dependencies: Uses only built-in list comprehension
- Maintainable: Clear, readable code
- Adequate performance: 100 tasks × 2 fields = 200 comparisons (sub-millisecond)

**Alternatives Considered**:
1. **Trie/prefix tree** for title search
   - Rejected: Over-engineering for ≤100 tasks, adds significant complexity
2. **Indexing with dictionary** (word → list[task_ids])
   - Rejected: Requires maintaining indexes on task updates (additional complexity)
3. **Full-text search library** (e.g., Whoosh)
   - Rejected: External dependency, overkill for in-memory <100 tasks

**Final Decision**: Linear scan (list comprehension) - meets SC-015 (500ms) with margin

---

### 4. Filter Implementation Approach

**Decision**: Chain of list comprehensions (status → priority → tag)

**Rationale**:
- Logical AND naturally expressed as chained filtering
- Pythonic: List comprehensions are idiomatic and fast
- O(n) total complexity (3 passes, but each pass is O(n))
- Maintainable: Each filter is clear, testable unit

**Alternatives Considered**:
1. **Single-pass with all conditions**
   ```python
   [t for t in tasks if
    (status_filter == FilterStatus.ALL or t.status == status_filter.value) and
    (not priority_filter or t.priority == priority_filter) and
    (not tag_filter or tag_filter in t.tags)]
   ```
   - Rejected: Complex conditional, harder to read and test
2. **SQL-like WHERE clause building**
   - Rejected: Over-engineering, adds abstraction without benefit
3. **Lazy evaluation with generators**
   - Rejected: No benefit when consuming entire list anyway

**Final Decision**: Chained list comprehensions for readability and maintainability

---

### 5. Sort Implementation Approach

**Decision**: Python built-in `list.sort()` with custom key function

**Rationale**:
- Stable sort (Timsort) preserves order for equal keys (FR-036)
- Built-in: No dependencies, optimal implementation
- O(n log n) complexity: Excellent performance even at 100 tasks
- Case-insensitive: `key=lambda t: t.title.lower()` handles requirement

**Alternatives Considered**:
1. **Custom sort implementation** (merge sort, quicksort)
   - Rejected: Re-inventing wheel, Python's sort is highly optimized
2. **Sorting by multiple keys** (e.g., priority then title)
   - Rejected: Not in specification (single sort criteria only)
3. **Sorted container** (bisect.insort for insertions)
   - Rejected: No requirement for maintaining sorted list, users sort on-demand

**Final Decision**: Python `list.sort()` with lambda key functions

---

### 6. CLI Menu Structure Extension

**Decision**: Add 5 new menu options (7-11) to existing 6-option menu

**Rationale**:
- Extends existing menu pattern (consistent UX)
- No structural changes needed (menu loop unchanged)
- Backward compatible (existing options 1-6 unchanged)
- Clear progression: Basic (1-6) → Intermediate (7-11)

**Alternatives Considered**:
1. **Submenu system** (Organization submenu with priority/tags/filter/sort)
   - Rejected: Extra navigation, violates "accessible through existing menu structure" (SC-010)
2. **Context menu** (right-click on task for options)
   - Rejected: Not CLI-appropriate, Phase I Basic has no context menus
3. **Replace existing options** (modify "Update task" to include priority/tags)
   - Rejected: Breaks backward compatibility (FR-037)

**Final Decision**: Extend existing menu with new options 7-11

---

### 7. Backward Compatibility Strategy

**Decision**: Default values in Task dataclass (priority=Medium, tags=[]) with `field(default_factory=list)`

**Rationale**:
- Seamless: Old code creating Task objects works with new fields auto-populated
- No migration logic needed: New fields have sensible defaults
- Type-safe: `field(default_factory=list)` creates new list per Task (avoids shared reference bug)
- Explicit: Users see Medium priority and no tags for old tasks

**Alternatives Considered**:
1. **Migration function** (scan and update old tasks)
   - Rejected: Unnecessary with default values, adds startup complexity
2. **Optional fields with None**
   - Rejected: Requires null checks throughout code, more complex
3. **Version flag in Task** (task_version=1 or 2)
   - Rejected: Over-engineering for simple additive extension

**Final Decision**: Default values in dataclass fields (no migration needed)

---

## Architecture Decisions

### Separation of Concerns

**Decision**: Maintain existing three-layer architecture (models → services → CLI)

**Rationale**:
- Extends existing pattern (no refactoring needed)
- Testable: Each layer can be unit tested independently
- Maintainable: Clear boundaries between data, logic, and UI
- Scalable: Future phases can add API layer without rework

### State Management

**Decision**: TaskService maintains single in-memory dictionary (no change)

**Rationale**:
- Matches Phase I Basic implementation
- Simple: No need for filter state persistence
- On-demand: Search/filter/sort create views, don't modify storage
- Efficient: No state synchronization overhead

---

## Technology Stack Decisions

### No New Dependencies

**Decision**: Use only Python 3.11+ standard library (dataclasses, enum, typing)

**Rationale**:
- Phase I scope: In-memory console app (no external complexity)
- Backward compatible: Matches existing dependency (none)
- Fast: No package installation, no version conflicts
- Maintainable: Standard library stable, well-documented

---

## Summary

All technical decisions made in this research phase:

1. ✅ Priority: Python `enum.Enum` (type-safe, user-friendly)
2. ✅ Tags: `list[str]` (simple, idiomatic)
3. ✅ Search: Linear scan with list comprehension (simple, fast enough)
4. ✅ Filter: Chained list comprehensions (readable, AND logic)
5. ✅ Sort: Python `list.sort()` (stable, optimized)
6. ✅ CLI: Extend existing menu (backward compatible)
7. ✅ Backward compatibility: Default values in dataclass (no migration)
8. ✅ Architecture: Maintain 3-layer structure (models → services → CLI)
9. ✅ Dependencies: None (standard library only)

**No [NEEDS CLARIFICATION] markers** - all decisions documented and justified.

**Next Step**: Proceed to Phase 1 design (data-model.md, contracts, quickstart.md)
