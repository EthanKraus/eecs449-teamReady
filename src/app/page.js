'use client'

import { useState } from 'react'
import axios from 'axios'
import Image from 'next/image'

// 配置参数
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.openai.com/v1/chat/completions'
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || 'your-api-key'
const MODEL = process.env.NEXT_PUBLIC_MODEL || 'gpt-3.5-turbo'

// 只需要机器人头像配置
const BOT_AVATAR = '/bot-avatar.png'

// 添加系统提示
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

export default function Home() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)

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
            SYSTEM_PROMPT,  // 添加系统提示
            ...messages,
            userMessage
          ],
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${API_KEY}`,
          },
        }
      )

      const aiMessage = response.data.choices[0].message
      setMessages((prev) => [...prev, aiMessage])
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
      setInput('')
    }
  }

  return (
    <div className="flex flex-col h-screen">
      {/* 顶部标题栏 */}
      <header className="flex items-center justify-center p-4 border-b">
        <h1 className="text-2xl font-bold">ShopSmart</h1>
      </header>

      {/* 主要聊天区域 */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full max-w-5xl mx-auto p-4">
          <div className="h-full overflow-y-auto">
            {messages.map((message, index) => (
              <div key={index} className={`mb-6 flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {message.role !== 'user' && (
                  <div className="w-8 h-8 rounded-full overflow-hidden mr-2 flex-shrink-0">
                    <Image src={BOT_AVATAR} alt="Bot" width={32} height={32} />
                  </div>
                )}
                <span className={`inline-block p-3 rounded-lg ${
                  message.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-100'
                }`}>
                  {message.content}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 底部输入区域 */}
      <div className="border-t p-4">
        <div className="max-w-5xl mx-auto">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
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
