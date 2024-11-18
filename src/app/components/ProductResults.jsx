
'use client'

export default function ProductResults({ results, summaries = [] }) {
  if (!results?.length) return null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      {results.map((result, index) => (
        <div 
          key={index} 
          style={{ 
            border: '1px solid #ccc', 
            borderRadius: '8px', 
            padding: '1rem', 
            display: 'flex', 
            gap: '1rem' 
          }}
        >
          <img 
            src={result.image} 
            alt={result.title} 
            style={{ 
              width: '100px', 
              height: 'auto', 
              borderRadius: '8px' 
            }} 
          />
          <div>
            <h3 style={{ margin: '0 0 0.5rem 0' }}>{result.title}</h3>
            <p style={{ margin: '0 0 0.5rem 0' }}>
              Price: ${result.price || 'N/A'}
            </p>
            <p style={{ margin: '0 0 0.5rem 0' }}>
              Rating: {result.rating}
            </p>
            {summaries[index]?.results && (
              <p style={{ margin: '0 0 0.5rem 0' }}>
                Summary: {summaries[index].results}
              </p>
            )}
            <a 
              href={result.product_url} 
              target="_blank" 
              rel="noopener noreferrer" 
              style={{ 
                color: '#007bff', 
                textDecoration: 'none' 
              }}
            >
              View Product
            </a>
          </div>
        </div>
      ))}
    </div>
  );
} 
