import React, { useMemo, useState, useEffect } from 'react';
import {
    Code2, Target, Filter, ArrowRight, Zap, Brain,
    Database, GitBranch, Hash, Network, Box, TrendingUp,
    Search, List, Layers, Activity, Workflow, Binary,
    ListTree, Share2, ArrowDownUp, Grid3x3, BookText,
    GitMerge, Repeat, Calculator, Plus, Blocks, Bookmark, X
} from 'lucide-react';
import ProgressStats from './ProgressStats';

const CodingSelection = ({ problems, onStartCoding, bookmarkedProblems = [] }) => {
    const [selectedCategory, setSelectedCategory] = React.useState(null);
    const [selectedDifficulty, setSelectedDifficulty] = React.useState(null);
    const [showBookmarked, setShowBookmarked] = useState(false);
    const progressStatsRef = React.useRef(null);
    const [searchQuery, setSearchQuery] = useState('');

    // Search autocomplete states
    const [searchResults, setSearchResults] = useState([]);
    const [selectedResultIndex, setSelectedResultIndex] = useState(0);
    const [showDropdown, setShowDropdown] = useState(false);

    // Bookmark hover tooltip
    const [isHoveringBookmark, setIsHoveringBookmark] = useState(false);

    // Get user ID from localStorage
    const getUserId = () => {
        try {
            const userStr = localStorage.getItem('aceit_user');
            if (!userStr) return null;
            const user = JSON.parse(userStr);
            return user?.id || user?.user_id || null;
        } catch (error) {
            console.error('Error parsing user from localStorage:', error);
            return null;
        }
    };
    const userId = getUserId();

    // Extract unique categories from all problem tags
    const categories = useMemo(() => {
        const tagSet = new Set();
        problems.forEach(problem => {
            if (problem.tags && Array.isArray(problem.tags)) {
                problem.tags.forEach(tag => tagSet.add(tag));
            }
        });
        return Array.from(tagSet).sort();
    }, [problems]);

    // Map categories to unique icons
    const categoryIcons = {
        'Array': Database,
        'String': Hash,
        'Hash Table': Box,
        'Dynamic Programming': Brain,
        'Math': Calculator,
        'Depth-First Search': GitBranch,
        'Breadth-First Search': Network,
        'Two Pointers': Target,
        'Binary Search': Search,
        'Greedy': Zap,
        'Linked List': List,
        'Stack': Layers,
        'Queue': Activity,
        'Tree': ListTree,
        'Graph': Share2,
        'Sorting': ArrowDownUp,
        'Backtracking': GitMerge,
        'Bit Manipulation': Binary,
        'Heap': Grid3x3,
        'Trie': BookText,
        'Sliding Window': Filter,
        'Divide and Conquer': Blocks,
        'Recursion': Repeat,
        'Prefix Sum': Plus,
        'Memoization': TrendingUp,
    };

    // Get filtered problem count
    const filteredCount = useMemo(() => {
        let filtered = showBookmarked
            ? problems.filter(p => bookmarkedProblems.includes(p.id))
            : problems;

        // Apply search filter
        if (searchQuery) {
            const query = searchQuery.toLowerCase();
            filtered = filtered.filter(p =>
                p.title.toLowerCase().includes(query) ||
                p.id.toLowerCase().includes(query) ||
                (p.tags && p.tags.some(tag => tag.toLowerCase().includes(query)))
            );
        }

        return filtered.filter(p => {
            const categoryMatch = !selectedCategory || (p.tags && p.tags.includes(selectedCategory));
            const difficultyMatch = !selectedDifficulty || p.difficulty === selectedDifficulty;
            return categoryMatch && difficultyMatch;
        }).length;
    }, [problems, selectedCategory, selectedDifficulty, showBookmarked, bookmarkedProblems, searchQuery]);

    // Get difficulty counts based on selected category
    const difficultyCounts = useMemo(() => {
        let filtered = showBookmarked
            ? problems.filter(p => bookmarkedProblems.includes(p.id))
            : problems;

        // Apply search filter
        if (searchQuery) {
            const query = searchQuery.toLowerCase();
            filtered = filtered.filter(p =>
                p.title.toLowerCase().includes(query) ||
                p.id.toLowerCase().includes(query) ||
                (p.tags && p.tags.some(tag => tag.toLowerCase().includes(query)))
            );
        }

        if (selectedCategory) {
            filtered = filtered.filter(p => p.tags && p.tags.includes(selectedCategory));
        }

        return {
            Easy: filtered.filter(p => p.difficulty === 'Easy').length,
            Medium: filtered.filter(p => p.difficulty === 'Medium').length,
            Hard: filtered.filter(p => p.difficulty === 'Hard').length,
        };
    }, [problems, selectedCategory, showBookmarked, bookmarkedProblems, searchQuery]);

    // Get category counts based on selected difficulty
    const getCategoryCount = (category) => {
        const filtered = selectedDifficulty
            ? problems.filter(p => p.difficulty === selectedDifficulty)
            : problems;

        return filtered.filter(p => p.tags && p.tags.includes(category)).length;
    };

    const handleStartCoding = () => {
        // Calculate filtered problems based on current selections
        let filtered = problems;

        if (showBookmarked) {
            filtered = problems.filter(p => bookmarkedProblems.includes(p.id));
        }

        if (selectedCategory) {
            filtered = filtered.filter(p => p.tags && p.tags.includes(selectedCategory));
        }

        if (selectedDifficulty) {
            filtered = filtered.filter(p => p.difficulty === selectedDifficulty);
        }

        onStartCoding({
            category: selectedCategory,
            difficulty: selectedDifficulty,
            showBookmarked: showBookmarked,
            context: 'filters',
            filteredProblems: filtered
        });
    };

    // Search autocomplete - filter results in real-time
    useEffect(() => {
        if (searchQuery.trim()) {
            const query = searchQuery.toLowerCase();
            const results = problems.filter(p =>
                p.title.toLowerCase().includes(query) ||
                p.id.toLowerCase().includes(query) ||
                (p.tags && p.tags.some(tag => tag.toLowerCase().includes(query)))
            ).slice(0, 10); // Limit to 10 results

            setSearchResults(results);
            setShowDropdown(results.length > 0);
            setSelectedResultIndex(0); // Reset selection
        } else {
            setSearchResults([]);
            setShowDropdown(false);
        }
    }, [searchQuery, problems]);

    // Handle selecting a problem from dropdown - navigate directly
    const handleSelectProblem = (problem) => {
        // Navigate directly to the problem without "Start Coding" button
        onStartCoding({
            ...problem,
            context: 'search',
            searchQuery: searchQuery,
            filteredProblems: searchResults // Pass the search results as filtered list
        });
        setShowDropdown(false);
        setSearchQuery('');
    };

    // Handle bookmark double-click - navigate to first bookmarked problem
    const handleBookmarkDoubleClick = () => {
        if (bookmarkedProblems.length > 0) {
            setShowBookmarked(true);
            setSelectedCategory(null);
            setSelectedDifficulty(null);
            // Get all bookmarked problems
            const bookmarkedList = problems.filter(p => bookmarkedProblems.includes(p.id));
            const firstBookmarked = bookmarkedList[0];
            if (firstBookmarked) {
                onStartCoding({
                    ...firstBookmarked,
                    context: 'bookmarks',
                    filteredProblems: bookmarkedList
                });
            }
        }
    };

    // Handle keyboard navigation in dropdown
    const handleKeyDown = (e) => {
        if (!showDropdown || searchResults.length === 0) return;

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            setSelectedResultIndex(prev =>
                prev < searchResults.length - 1 ? prev + 1 : prev
            );
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            setSelectedResultIndex(prev => prev > 0 ? prev - 1 : 0);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (searchResults[selectedResultIndex]) {
                handleSelectProblem(searchResults[selectedResultIndex]);
            }
        } else if (e.key === 'Escape') {
            setShowDropdown(false);
        }
    };


    const handleSkipFilters = () => {
        onStartCoding({
            category: null,
            difficulty: null,
            showBookmarked: false
        });
    };

    return (
        <div className="min-h-screen p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-bold text-gray-800 mb-3 flex items-center justify-center gap-3">
                        <Code2 className="w-10 h-10 text-blue-600" />
                        CodeSprint
                    </h1>
                    <p className="text-gray-600 text-lg max-w-3xl mx-auto">
                        Level up with smart practice and real coding challenges.
                    </p>
                </div>

                {/* Progress Stats Section */}
                <ProgressStats ref={progressStatsRef} userId={userId} />

                {/* Search Bar with Autocomplete */}
                <div className="mb-8 max-w-2xl mx-auto">
                    <div className="relative">
                        <input
                            type="text"
                            placeholder="Search problems by title, ID, or tags..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            onKeyDown={handleKeyDown}
                            className="w-full px-4 py-3 pl-12 pr-16 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-base shadow-sm"
                        />
                        <Search className="w-5 h-5 text-gray-400 absolute left-4 top-3.5" />

                        {/* Clear Button */}
                        {searchQuery && (
                            <button
                                onClick={() => { setSearchQuery(''); setShowDropdown(false); }}
                                className="absolute right-12 top-3 p-1 hover:bg-gray-100 rounded"
                                title="Clear search"
                            >
                                <X className="w-5 h-5 text-gray-500" />
                            </button>
                        )}

                        {/* Bookmark Icon */}
                        <button
                            onDoubleClick={handleBookmarkDoubleClick}
                            onMouseEnter={() => setIsHoveringBookmark(true)}
                            onMouseLeave={() => setIsHoveringBookmark(false)}
                            className="absolute right-3 top-2.5 p-1.5 rounded hover:bg-blue-50 transition-colors"
                        >
                            <Bookmark
                                className={`w-5 h-5 ${showBookmarked || bookmarkedProblems.length > 0
                                    ? 'fill-blue-600 text-blue-600'
                                    : 'text-gray-400'
                                    }`}
                            />
                            {bookmarkedProblems.length > 0 && (
                                <span className="absolute -top-1 -right-1 bg-blue-600 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center">
                                    {bookmarkedProblems.length}
                                </span>
                            )}
                        </button>

                        {/* Bookmark Tooltip */}
                        {isHoveringBookmark && (
                            <div className="absolute right-0 top-14 bg-gray-900 text-white text-xs px-3 py-1.5 rounded shadow-lg whitespace-nowrap z-50">
                                Double-click to view bookmarked problems
                            </div>
                        )}

                        {/* Autocomplete Dropdown */}
                        {showDropdown && searchResults.length > 0 && (
                            <div className="absolute top-full left-0 right-0 bg-white border-2 border-gray-300 rounded-xl mt-2 shadow-xl z-50 max-h-96 overflow-y-auto">
                                {searchResults.map((problem, index) => (
                                    <div
                                        key={problem.id}
                                        onClick={() => handleSelectProblem(problem)}
                                        className={`p-4 cursor-pointer border-b border-gray-100 last:border-b-0 transition-colors ${index === selectedResultIndex
                                            ? 'bg-blue-50'
                                            : 'hover:bg-blue-50'
                                            }`}
                                    >
                                        <div className="flex items-start justify-between">
                                            <div className="flex-1">
                                                <div className="font-semibold text-gray-800">{problem.title}</div>
                                                <div className="text-xs text-gray-500 mt-1">{problem.id}</div>
                                            </div>
                                            <span className={`ml-3 px-2 py-1 rounded text-xs font-medium ${problem.difficulty === 'Easy'
                                                ? 'bg-green-100 text-green-700' :
                                                problem.difficulty === 'Medium'
                                                    ? 'bg-yellow-100 text-yellow-700' :
                                                    'bg-red-100 text-red-700'
                                                }`}>
                                                {problem.difficulty}
                                            </span>
                                        </div>
                                        {problem.tags && problem.tags.length > 0 && (
                                            <div className="flex gap-1 mt-2">
                                                {problem.tags.slice(0, 3).map(tag => (
                                                    <span key={tag} className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
                                                        {tag}
                                                    </span>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>


                {/* Category Selection */}
                <div className="mb-12">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-6 flex items-center gap-2">
                        <Target className="w-6 h-6 text-blue-600" />
                        Category
                    </h2>
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-5">
                        {/* All Categories Option */}
                        <button
                            onClick={() => setSelectedCategory(null)}
                            className={`p - 5 rounded - xl border - 2 transition - all duration - 200 ${selectedCategory === null
                                ? 'bg-blue-600 border-blue-600 text-white shadow-lg scale-105'
                                : 'bg-white border-gray-200 text-gray-700 hover:border-blue-300 hover:shadow-md'
                                } `}
                        >
                            <div className="flex flex-col items-center gap-2">
                                <Code2 className="w-7 h-7" />
                                <span className="font-semibold text-sm">All Categories</span>
                                <span className="text-xs opacity-80">{problems.length} problems</span>
                            </div>
                        </button>

                        {/* Individual Categories */}
                        {categories.map((category) => {
                            const IconComponent = categoryIcons[category] || Code2;
                            const count = getCategoryCount(category);

                            return (
                                <button
                                    key={category}
                                    onClick={() => setSelectedCategory(category)}
                                    disabled={count === 0}
                                    className={`p - 5 rounded - xl border - 2 transition - all duration - 200 ${selectedCategory === category
                                        ? 'bg-blue-600 border-blue-600 text-white shadow-lg scale-105'
                                        : count === 0
                                            ? 'bg-gray-50 border-gray-200 text-gray-400 cursor-not-allowed'
                                            : 'bg-white border-gray-200 text-gray-700 hover:border-blue-300 hover:shadow-md'
                                        } `}
                                >
                                    <div className="flex flex-col items-center gap-2">
                                        <IconComponent className="w-7 h-7" />
                                        <span className="font-semibold text-sm text-center leading-tight">{category}</span>
                                        <span className="text-xs opacity-80">{count} problems</span>
                                    </div>
                                </button>
                            );
                        })}
                    </div>
                </div>

                {/* Difficulty Selection */}
                <div className="mb-12">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
                        <Filter className="w-6 h-6 text-blue-600" />
                        Difficulty
                    </h2>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {/* All Difficulties Option */}
                        <button
                            onClick={() => setSelectedDifficulty(null)}
                            className={`p - 6 rounded - xl border - 2 transition - all duration - 200 ${selectedDifficulty === null
                                ? 'bg-blue-600 border-blue-600 text-white shadow-lg scale-105'
                                : 'bg-white border-gray-200 text-gray-700 hover:border-blue-300 hover:shadow-md'
                                } `}
                        >
                            <div className="flex flex-col items-center gap-3">
                                <Zap className="w-8 h-8" />
                                <span className="font-semibold">All Levels</span>
                                <span className="text-sm opacity-80">
                                    {difficultyCounts.Easy + difficultyCounts.Medium + difficultyCounts.Hard} problems
                                </span>
                            </div>
                        </button>

                        {/* Easy */}
                        <button
                            onClick={() => setSelectedDifficulty('Easy')}
                            disabled={difficultyCounts.Easy === 0}
                            className={`p - 6 rounded - xl border - 2 transition - all duration - 200 ${selectedDifficulty === 'Easy'
                                ? 'bg-green-600 border-green-600 text-white shadow-lg scale-105'
                                : difficultyCounts.Easy === 0
                                    ? 'bg-gray-50 border-gray-200 text-gray-400 cursor-not-allowed'
                                    : 'bg-white border-green-200 text-green-700 hover:border-green-400 hover:shadow-md'
                                } `}
                        >
                            <div className="flex flex-col items-center gap-3">
                                <span className="text-3xl">🟢</span>
                                <span className="font-semibold">Easy</span>
                                <span className="text-sm opacity-80">{difficultyCounts.Easy} problems</span>
                            </div>
                        </button>

                        {/* Medium */}
                        <button
                            onClick={() => setSelectedDifficulty('Medium')}
                            disabled={difficultyCounts.Medium === 0}
                            className={`p - 6 rounded - xl border - 2 transition - all duration - 200 ${selectedDifficulty === 'Medium'
                                ? 'bg-yellow-600 border-yellow-600 text-white shadow-lg scale-105'
                                : difficultyCounts.Medium === 0
                                    ? 'bg-gray-50 border-gray-200 text-gray-400 cursor-not-allowed'
                                    : 'bg-white border-yellow-200 text-yellow-700 hover:border-yellow-400 hover:shadow-md'
                                } `}
                        >
                            <div className="flex flex-col items-center gap-3">
                                <span className="text-3xl">🟡</span>
                                <span className="font-semibold">Medium</span>
                                <span className="text-sm opacity-80">{difficultyCounts.Medium} problems</span>
                            </div>
                        </button>

                        {/* Hard */}
                        <button
                            onClick={() => setSelectedDifficulty('Hard')}
                            disabled={difficultyCounts.Hard === 0}
                            className={`p - 6 rounded - xl border - 2 transition - all duration - 200 ${selectedDifficulty === 'Hard'
                                ? 'bg-red-600 border-red-600 text-white shadow-lg scale-105'
                                : difficultyCounts.Hard === 0
                                    ? 'bg-gray-50 border-gray-200 text-gray-400 cursor-not-allowed'
                                    : 'bg-white border-red-200 text-red-700 hover:border-red-400 hover:shadow-md'
                                } `}
                        >
                            <div className="flex flex-col items-center gap-3">
                                <span className="text-3xl">🔴</span>
                                <span className="font-semibold">Hard</span>
                                <span className="text-sm opacity-80">{difficultyCounts.Hard} problems</span>
                            </div>
                        </button>
                    </div>
                </div>

                {/* Bottom Action Bar - Improved */}
                <div className="bg-white rounded-xl shadow-lg border-2 border-gray-100 p-8 mt-8">
                    <div className="flex flex-col items-center gap-6">
                        {/* Problem Count Display */}
                        <div className="text-center space-y-2">
                            {filteredCount > 0 ? (
                                <>
                                    <div className="flex items-baseline justify-center gap-2">
                                        <span className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
                                            {filteredCount}
                                        </span>
                                        <span className="text-xl text-gray-600 font-medium">
                                            problem{filteredCount !== 1 ? 's' : ''} available
                                        </span>
                                    </div>
                                    {(selectedCategory || selectedDifficulty) && (
                                        <div className="flex items-center justify-center gap-2 flex-wrap">
                                            {selectedCategory && (
                                                <span className="bg-blue-100 text-blue-700 px-4 py-1.5 rounded-full text-sm font-medium">
                                                    {selectedCategory}
                                                </span>
                                            )}
                                            {selectedDifficulty && (
                                                <span className={`px-4 py-1.5 rounded-full text-sm font-medium ${selectedDifficulty === 'Easy' ? 'bg-green-100 text-green-700' :
                                                    selectedDifficulty === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                                                        'bg-red-100 text-red-700'
                                                    }`}>
                                                    {selectedDifficulty}
                                                </span>
                                            )}
                                        </div>
                                    )}
                                </>
                            ) : (
                                <p className="text-xl text-red-600 font-medium">
                                    No problems match your selection
                                </p>
                            )}
                        </div>

                        {/* Action Buttons */}
                        <div className="flex flex-col gap-3 w-full max-w-md">
                            <button
                                onClick={handleStartCoding}
                                disabled={filteredCount === 0}
                                className={`px-8 py-4 rounded-xl font-semibold text-lg flex items-center justify-center gap-3 transition-all shadow-md ${filteredCount === 0
                                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                                    : 'bg-gradient-to-r from-blue-600 to-blue-700 text-white hover:from-blue-700 hover:to-blue-800 hover:shadow-xl hover:scale-105 active:scale-100'
                                    }`}
                            >
                                Start Coding
                                <ArrowRight className="w-6 h-6" />
                            </button>

                            <button
                                onClick={handleSkipFilters}
                                className="text-blue-600 hover:text-blue-800 text-sm font-medium py-2 hover:underline transition-all"
                            >
                                Skip & See All Problems
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CodingSelection;
