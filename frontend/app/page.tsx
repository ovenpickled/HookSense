import React from 'react';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-24 bg-gray-900 text-white">
      <h1 className="text-4xl font-bold mb-8">AI Code Reviewer Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-6xl">
        {/* Metrics Cards */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold mb-2">Total Reviews</h2>
          <p className="text-4xl font-bold text-blue-400">124</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold mb-2">Issues Found</h2>
          <p className="text-4xl font-bold text-red-400">45</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold mb-2">Avg. Review Time</h2>
          <p className="text-4xl font-bold text-green-400">1.2s</p>
        </div>

        {/* Recent Activity */}
        <div className="col-span-1 md:col-span-3 bg-gray-800 p-6 rounded-lg shadow-lg mt-6">
          <h2 className="text-2xl font-semibold mb-4">Recent Reviews</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="pb-2">Repository</th>
                  <th className="pb-2">PR #</th>
                  <th className="pb-2">Status</th>
                  <th className="pb-2">Date</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-gray-700/50">
                  <td className="py-2">owner/repo-a</td>
                  <td className="py-2">#42</td>
                  <td className="py-2 text-green-400">Completed</td>
                  <td className="py-2">2023-10-27</td>
                </tr>
                <tr className="border-b border-gray-700/50">
                  <td className="py-2">owner/repo-b</td>
                  <td className="py-2">#15</td>
                  <td className="py-2 text-yellow-400">Pending</td>
                  <td className="py-2">2023-10-27</td>
                </tr>
                <tr>
                  <td className="py-2">owner/repo-a</td>
                  <td className="py-2">#41</td>
                  <td className="py-2 text-red-400">Failed</td>
                  <td className="py-2">2023-10-26</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  );
}
