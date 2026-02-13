import React from 'react';
import { AlertCircle, CheckCircle, XCircle } from 'lucide-react';

const TestResultsDisplay = ({ testResults, output }) => {
    if (!testResults) {
        return (
            <pre className="p-4 bg-gray-50 text-sm min-h-[120px] max-h-60 overflow-y-auto whitespace-pre-wrap font-mono">
                {output || "Click 'Run Code' to test your solution..."}
            </pre>
        );
    }

    // Parse the output to extract individual test results if available
    const renderVisualDiff = (expected, actual) => {
        const expectedStr = JSON.stringify(expected, null, 2);
        const actualStr = JSON.stringify(actual, null, 2);

        return (
            <div className="grid grid-cols-2 gap-4 mt-2 text-xs">
                <div className="bg-red-50 border border-red-200 rounded p-2">
                    <div className="font-semibold text-red-700 mb-1">Expected:</div>
                    <pre className="text-red-800 whitespace-pre-wrap">{expectedStr}</pre>
                </div>
                <div className="bg-orange-50 border border-orange-200 rounded p-2">
                    <div className="font-semibold text-orange-700 mb-1">Actual:</div>
                    <pre className="text-orange-800 whitespace-pre-wrap">{actualStr}</pre>
                </div>
            </div>
        );
    };

    return (
        <div className="space-y-3">
            {/* Summary Bar */}
            <div className="p-3 bg-gray-50 border-b">
                <div className="flex justify-between items-center mb-1">
                    <div className="flex items-center gap-2">
                        <span className="font-medium">Test Results:</span>
                        {testResults.action === 'run' && testResults.hiddenCount > 0 && (
                            <span className="text-xs text-gray-500">
                                ({testResults.visibleCount} visible, {testResults.hiddenCount} hidden)
                            </span>
                        )}
                        {testResults.isSolved && (
                            <span className="text-green-600 font-bold text-sm flex items-center gap-1">
                                <CheckCircle className="w-4 h-4" /> Solved!
                            </span>
                        )}
                    </div>
                    <span className={`font-bold flex items-center gap-1 ${testResults.passed === testResults.total ? 'text-green-600' : 'text-red-600'
                        }`}>
                        {testResults.passed === testResults.total ? (
                            <CheckCircle className="w-4 h-4" />
                        ) : (
                            <AlertCircle className="w-4 h-4" />
                        )}
                        {testResults.passed}/{testResults.total} passed ({testResults.percentage}%)
                    </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                        className={`h-2 rounded-full transition-all ${testResults.percentage >= 80
                            ? 'bg-green-600'
                            : testResults.percentage >= 60
                                ? 'bg-yellow-500'
                                : 'bg-red-500'
                            }`}
                        style={{ width: `${testResults.percentage}%` }}
                    ></div>
                </div>
            </div>

            {/* Detailed Test Cases */}
            {testResults.details && testResults.details.length > 0 ? (
                <div className="max-h-96 overflow-y-auto space-y-2 p-4">
                    {testResults.details.map((test, idx) => (
                        <div
                            key={idx}
                            className={`border-l-4 p-3 rounded ${test.passed
                                ? 'bg-green-50 border-green-500'
                                : 'bg-red-50 border-red-500'
                                }`}
                        >
                            <div className="flex items-start justify-between mb-2">
                                <div className="flex items-center gap-2">
                                    {test.passed ? (
                                        <CheckCircle className="w-5 h-5 text-green-600" />
                                    ) : (
                                        <XCircle className="w-5 h-5 text-red-600" />
                                    )}
                                    <span className="font-semibold">
                                        Test {idx + 1}: {test.description || 'Test case'}
                                    </span>
                                </div>
                                <span
                                    className={`text-xs px-2 py-1 rounded ${test.passed
                                        ? 'bg-green-100 text-green-700'
                                        : 'bg-red-100 text-red-700'
                                        }`}
                                >
                                    {test.passed ? 'Passed' : 'Failed'}
                                </span>
                            </div>

                            {test.scenario && (
                                <p className="text-sm text-gray-600 mb-2 italic">{test.scenario}</p>
                            )}

                            <div className="text-sm space-y-1">
                                <div>
                                    <span className="font-medium">Input:</span>{' '}
                                    <code className="bg-gray-100 px-2 py-0.5 rounded text-xs">
                                        {JSON.stringify(test.input)}
                                    </code>
                                </div>

                                {!test.passed && (
                                    <>
                                        {renderVisualDiff(test.expected, test.actual)}
                                        {test.error && (
                                            <div className="mt-2 p-2 bg-red-100 border border-red-300 rounded text-xs">
                                                <span className="font-semibold text-red-700">Error: </span>
                                                <span className="text-red-800">{test.error}</span>
                                            </div>
                                        )}
                                    </>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <pre className="p-4 bg-gray-50 text-sm min-h-[120px] max-h-60 overflow-y-auto whitespace-pre-wrap font-mono">
                    {output}
                </pre>
            )}
        </div>
    );
};

export default TestResultsDisplay;
