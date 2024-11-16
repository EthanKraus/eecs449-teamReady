'use client'

import { useState, useEffect } from 'react'
import { useState, useEffect } from 'react'
import axios from 'axios'
import Image from 'next/image'
import Login from './login'
import ChangePassword from './change_password'

// API Configuration
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.openai.com/v1/chat/completions'
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || 'your-api-key'
const MODEL = process.env.NEXT_PUBLIC_MODEL || 'gpt-3.5-turbo'

// Bot Avatar Configuration
const BOT_AVATAR = '/bot-avatar-bg.png'

// System Prompt Configuration
const SYSTEM_PROMPT = {
  role: 'system',
  content: `You are ShopSmart, a professional shopping assistant. Your responsibilities include:
  1. Helping users make informed purchase decisions
  2. Comparing different products and their features
  3. Answering specific questions about products
  4. Recommending items based on user needs
  5. Providing money-saving tips and smart shopping advice

  Always maintain:
  - A professional and friendly demeanor
  - Specific and practical recommendations
  - Ask for clarification when needed to provide better advice
  - Consider user's budget and specific requirements
  - Stay honest and objective, avoid overselling

  When responding:
  - Use clear and concise language
  - Provide structured comparisons when comparing products
  - Include price ranges when discussing products
  - Mention important factors like quality, durability, and value for money
  - Share relevant tips about timing of purchases (sales, seasonal discounts, etc.)
  - Suggest alternatives when appropriate`
}

export default function Page() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [isAuthenticated, setIsAuthenticated] = useState(true);
  const [isChangingPassword, setIsChangingPassword] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/auth', {withCredentials: true,})
        if (response.data.username) {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false)
        }
      } catch (error) {
        console.error('Error checking authentication status:', error);
        setIsAuthenticated(false); // On error, treat as not authenticated
      }
    };

    checkAuth();
  }, []);

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
    e.preventDefault()
    if (!input.trim()) return

    setIsLoading(true)
    const userMessage = { role: 'user', content: input }
    setMessages((prev) => [...prev, userMessage])

    try {
      const response = await axios.post(
        API_URL,
        {
          model: MODEL,
          messages: [
            SYSTEM_PROMPT,  // Add system prompt
            ...messages,
            userMessage
          ],
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${API_KEY}`,
            credentials: 'include'
          },
        }
      )

      const aiMessage = response.data.choices[0].message
      setMessages((prev) => [...prev, aiMessage])
    } catch (error) {
      console.error('Error:', error.response ? error.response.data : error.message)
    } finally {
      setIsLoading(false)
      setInput('')
    }
  }

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]); // Trigger this effect when messages change

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  if (isChangingPassword) {
    return <ChangePassword onCancel={() => setIsChangingPassword(false)} />;
  }

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
          <button
            onClick={handleChangePassword}
            className="bg-yellow-500 text-white p-2 rounded-full hover:bg-yellow-600 transition-colors"
          >
            Change Password
          </button>

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
          <div
            className="h-full overflow-y-auto"
            ref={chatContainerRef}
          >
            {messages.map((message, index) => (
              <div key={index} className={`mb-6 flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {message.role !== 'user' && (
                  <div className="w-12 h-12 flex items-center justify-center rounded-full overflow-hidden mr-2 flex-shrink-0">
                    <Image src={BOT_AVATAR} alt="Bot" width={48} height={48} />
                  </div>
                )}
                <span className={`inline-block p-3 rounded-lg ${message.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-300  dark:bg-zinc-800 dark:text-gray-200'
                  }`}>
                  {message.content}
                </span>
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