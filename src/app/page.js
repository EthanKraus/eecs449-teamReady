'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import Image from 'next/image'
import Login from './login'
import ChangePassword from './change_password'
import ProductResults from './components/ProductResults'

// 配置参数
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.openai.com/v1/chat/completions'
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || 'your-api-key'
const MODEL = process.env.NEXT_PUBLIC_MODEL || 'gpt-3.5-turbo'

// 只需要机器人头像配置
const BOT_AVATAR = '/bot-avatar-bg.png'

// 添加系统提示
const SYSTEM_PROMPT = {
  role: 'system',
  content: `You are ShopSmart, a professional shopping assistant. You MUST follow these rules:

  1. When a user provides product details or confirms a search, IMMEDIATELY respond with ONLY this JSON:
     {"type": "search", "category": "clothing", "keyword": "search terms", "max_limit": "price"}
     No other text allowed.

  2. For review requests:
     {"type": "review_request", "index": number}
     No other text allowed.

  3. Only engage in conversation when:
     - Asking for clarification about budget
     - Asking about specific preferences
     - Asking about the occasion
     Do not acknowledge with conversation when user is ready to search.

  Examples:
  User: "100-300 dollars"
  Response: {"type": "search", "category": "clothing", "keyword": "red shiny dress", "max_limit": "300"}

  User: "Show me red dresses"
  Response: {"type": "search", "category": "clothing", "keyword": "red dress", "max_limit": "100"}
  
  User: "What do people say about the first product?"
  Response: {"type": "review_request", "index": 0}
  
  User: "Can you clarify the price range?"
  Response: Could you please specify your budget for this item?`
};

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export default function Home() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [isAuthenticated, setIsAuthenticated] = useState(true);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [productResults, setProductResults] = useState([]);
  const [lastProductResults, setLastProductResults] = useState([]);

  // useEffect(() => {
  //   const checkAuth = async () => {
  //     try {
  //       const response = await axios.get('http://127.0.0.1:5000/auth', {withCredentials: true,})
  //       if (response.data.username) {
  //         setIsAuthenticated(true);
  //       } else {
  //         setIsAuthenticated(false)
  //       }
  //     } catch (error) {
  //       console.error('Error checking authentication status:', error);
  //       setIsAuthenticated(false); // On error, treat as not authenticated
  //     }
  //   };

  //   checkAuth();
  // }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/logout', {withCredentials: true,})
      if (response.status === 200) {
        setIsAuthenticated(false)
      }
    } catch (error) {
      console.error('Error logging out:', error)
    }
  }

  const handleChangePassword = () => {
    setIsChangingPassword(true)  // Set flag to show ChangePassword component
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setIsLoading(true);
    setMessages(prev => [...prev, { role: 'user', content: input }]);

    try {
      const aiResponse = await axios.post(API_URL, {
        model: MODEL,
        messages: [SYSTEM_PROMPT, ...messages, { role: 'user', content: input }]
      }, {
        headers: {
          'Authorization': `Bearer ${API_KEY}`
        }
      });

      const aiMessage = aiResponse.data.choices[0].message;

      // Try to parse the response as JSON
      try {
        const parsedResponse = JSON.parse(aiMessage.content);
        
        if (parsedResponse.type === 'search') {
          const scraperParams = {
            category: parsedResponse.category,
            keyword: parsedResponse.keyword,
            max_links_num: 10
          };

          console.log("Sending to backend:", scraperParams);

          const scraperResponse = await axios.post(
            `${BACKEND_URL}/scrape`,
            scraperParams,
            {
              headers: {
                'Content-Type': 'application/json'
              }
            }
          );

          console.log("Backend response:", scraperResponse.data);

          // Store the results for the ProductResults component to use
          setProductResults(scraperResponse.data.results);
          setLastProductResults(scraperResponse.data.results);

          // Add a message indicating search results are ready
          setMessages(prev => [
            ...prev,
            {
              role: 'assistant',
              content: 'PRODUCT_RESULTS_PLACEHOLDER', // Special marker for rendering
              results: scraperResponse.data.results // Store results with the message
            }
          ]);
        } else if (parsedResponse.type === 'review_request') {
          const productIndex = parsedResponse.index;
          
          console.log("Last product results:", lastProductResults); // Debug log
          
          if (!lastProductResults || !lastProductResults[productIndex]) {
            setMessages(prev => [...prev, {
              role: 'assistant',
              content: 'Please search for products first before requesting reviews.'
            }]);
            return;
          }

          const product = lastProductResults[productIndex];
          console.log("Requesting review for product:", product); // Debug log

          try {
            const reviewResponse = await axios.post(
              `${BACKEND_URL}/scrape_summary`,
              { ASIN: product.ASIN },
              {
                headers: {
                  'Content-Type': 'application/json'
                }
              }
            );

            if (reviewResponse.data && reviewResponse.data.results) {
              setMessages(prev => [...prev, {
                role: 'assistant',
                content: `Here's what people are saying about this product: ${reviewResponse.data.results}`
              }]);
            } else {
              throw new Error('Invalid response format from server');
            }
          } catch (error) {
            // More robust error logging
            console.error('Error details:', {
              message: error.message || 'No error message',
              response: error.response ? {
                data: error.response.data || null,
                status: error.response.status || null
              } : null,
              fullError: error
            });

            // More descriptive error message to user
            const errorMessage = error.response?.data?.message 
              || error.message 
              || 'An unknown error occurred';

            setMessages(prev => [...prev, {
              role: 'assistant',
              content: `Sorry, I encountered an error fetching the reviews. Details: ${errorMessage}`
            }]);
          } finally {
            setIsLoading(false);
          }
        } else {
          // Not a search query or review request, just add the response to chat
          setMessages(prev => [...prev, aiMessage]);
        }
      } catch (parseError) {
        // Not JSON, just a regular conversation response
        setMessages(prev => [...prev, aiMessage]);
      }
    } catch (error) {
      console.error('Error:', error)
      setMessages((prev) => [
        ...prev,
        { 
          role: 'assistant', 
          content: 'Sorry, I encountered an error processing your request.' 
        }
      ])
    } finally {
      setIsLoading(false)
      setInput('')
    }
  }

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

//   if (isChangingPassword) {
//     return <ChangePassword onCancel={() => setIsChangingPassword(false)} />;
//   }

  return (
    <div className="flex flex-col h-screen">
      {/* 顶部标题栏 */}
      <header className="flex items-left justify-left p-4 border-b dark:border-zinc-800">
        <div className="w-12 h-12 flex items-center justify-center rounded-full overflow-hidden mr-2 flex-shrink-0 ml-1">
          <Image src={BOT_AVATAR} alt="Bot" width={48} height={48} />
        </div>
        <h1 className="text-2xl flex items-center justify-center font-normal ml-2 dark:text-white">ShopSmart</h1>
      
        <div className="absolute top-4 right-4 flex gap-2">
          {/* Change Password Button */}
          {/* <button
            onClick={handleChangePassword}
            className="bg-yellow-500 text-white p-2 rounded-full hover:bg-yellow-600 transition-colors"
          >
            Change Password
          </button> */}

          {/* Logout button */}
          <button
            onClick={handleLogout}
            className="bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition-colors"
          >
            Logout
          </button>
        </div>
      </header>

      {/* 主要聊天区域 */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full max-w-5xl mx-auto p-4">
          <div className="h-full overflow-y-auto">
            {messages.map((message, index) => (
              <div key={index} className={`mb-6 flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {message.role !== 'user' && (
                  <div className="w-12 h-12 flex items-center justify-center rounded-full overflow-hidden mr-2 flex-shrink-0">
                    <Image src={BOT_AVATAR} alt="Bot" width={48} height={48} />
                  </div>
                )}
                <div className={`inline-block p-3 rounded-lg ${
                  message.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-300 dark:bg-zinc-800 dark:text-gray-200'
                }`}>
                  {message.content === 'PRODUCT_RESULTS_PLACEHOLDER' ? (
                    <div key={`product-results-${index}`}>
                      <ProductResults 
                        results={message.results} 
                        setLastProductResults={setLastProductResults}
                      />
                    </div>
                  ) : (
                    <div key={`message-${index}`}>
                      {message.content}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 底部输入区域 */}
      <div className="border-t dark:border-zinc-800 p-4">
        <div className="max-w-5xl mx-auto">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 p-3 border border-gray-300  dark:border-zinc-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-zinc-100 dark:bg-zinc-900 dark:text-gray-200"
            />
            <button
              type="submit"
              disabled={isLoading}
              className="px-4 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-blue-300 transition-colors"
            >
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
