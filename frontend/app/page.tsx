"use client";
import React, { useEffect, useState } from 'react';

export default function Home() {
  const [metrics, setMetrics] = useState({ total_reviews: 0, issues_found: 0, avg_review_time: "0s" });
  const [reviews, setReviews] = useState([]);
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  useEffect(() => {
    fetch(`${apiUrl}/metrics`)
      .then(res => res.json())
      .then(data => setMetrics(data))
      .catch(err => console.error("Failed to fetch metrics", err));

    fetch(`${apiUrl}/reviews`)
      .then(res => res.json())
      .then(data => setReviews(data))
      .catch(err => console.error("Failed to fetch reviews", err));
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center p-24 bg-gray-900 text-white">
      <h1 className="text-4xl font-bold mb-8">AI Code Reviewer Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-6xl">
        {/* Metrics Cards */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold mb-2">Total Reviews</h2>
          <p className="text-4xl font-bold text-blue-400">{metrics.total_reviews}</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold mb-2">Issues Found</h2>
          <p className="text-4xl font-bold text-red-400">{metrics.issues_found}</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold mb-2">Avg. Review Time</h2>
          <p className="text-4xl font-bold text-green-400">{metrics.avg_review_time}</p>
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
                {reviews.map((review: any, i) => (
                  <tr key={i} className="border-b border-gray-700/50">
                    <td className="py-2">{review.repository}</td>
                    <td className="py-2">#{review.pr_number}</td>
                    <td className={`py-2 ${review.status === 'completed' ? 'text-green-400' : 'text-yellow-400'}`}>
                      {review.status}
                    </td>
                    <td className="py-2">{review.date}</td>
                  </tr>
                ))}
                {reviews.length === 0 && (
                  <tr>
                    <td colSpan={4} className="py-4 text-center text-gray-500">No reviews yet</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  );
}
