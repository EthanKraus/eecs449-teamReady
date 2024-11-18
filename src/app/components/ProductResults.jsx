'use client'

import React, { useEffect, useState } from 'react';

export default function ProductResults({ results, setLastProductResults }) {
  // Move the state update to useEffect
  useEffect(() => {
    if (results && results.length > 0) {
      // Filter out duplicates based on ASIN
      const uniqueResults = results.filter((product, index, self) =>
        index === self.findIndex((p) => p.ASIN === product.ASIN)
      );
      setLastProductResults(uniqueResults);
    }
  }, [results, setLastProductResults]);

  // Add null check and loading state
  if (!results) {
    return <div>Loading...</div>;
  }

  // Filter out duplicates before rendering
  const uniqueResults = results.filter((product, index, self) =>
    index === self.findIndex((p) => p.ASIN === product.ASIN)
  );

  if (uniqueResults.length === 0) {
    return <div>No results found</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {uniqueResults.map((product, index) => (
        <div key={`${product.ASIN}-${index}`} className="border rounded-lg p-4 dark:border-zinc-800">
          {product.image && (
            <img 
              src={product.image} 
              alt={product.title || 'Product image'}
              className="w-full h-48 object-cover rounded-lg mb-4"
            />
          )}
          <h3 className="font-medium mb-2">{product.title}</h3>
          <p className="text-lg font-bold">${product.price}</p>
          <p className="text-sm">Rating: {product.rating}</p>
          {product.product_url && (
            <a 
              href={product.product_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline mt-2 block"
            >
              View Product
            </a>
          )}
        </div>
      ))}
    </div>
  );
} 