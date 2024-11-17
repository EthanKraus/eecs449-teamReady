export default function ProductResults({ results }) {
  if (!results || results.length === 0) {
    return <div>No results found</div>;
  }

  return (
    <div className="flex flex-col gap-4">
      {results.map((result, index) => (
        <div key={index} className="border border-gray-200 rounded-lg p-4 flex gap-4">
          <img 
            src={result.image} 
            alt={result.title} 
            className="w-24 h-auto rounded-lg"
          />
          <div>
            <h3 className="font-medium">{result.title}</h3>
            <p>Price: {result.price ? `$${result.price}` : 'N/A'}</p>
            <p>Rating: {result.rating}</p>
            <a 
              href={result.product_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              View Product
            </a>
          </div>
        </div>
      ))}
    </div>
  );
} 