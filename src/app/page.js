'use client'

import { useState } from 'react'
import axios from 'axios'
import Image from 'next/image'

// 配置参数
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.openai.com/v1/chat/completions'
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || 'your-api-key'
const MODEL = process.env.NEXT_PUBLIC_MODEL || 'gpt-3.5-turbo'

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
          messages: [...messages, userMessage],
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
    <div className="flex flex-col items-center justify-center min-h-screen p-8">
      <h1 className="text-2xl font-bold mb-4">XX</h1>
      <div className="w-full max-w-md p-4 bg-white rounded-lg shadow-md">
        <div className="mb-4 h-64 overflow-y-auto border border-gray-300 rounded p-2">
          {messages.map((message, index) => (
            <div key={index} className={`mb-2 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
              <span className={`inline-block p-2 rounded ${message.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
                {message.content}
              </span>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="XXX"
            className="flex-grow p-2 border border-gray-300 rounded-l"
          />
          <button
            type="submit"
            disabled={isLoading}
            className="bg-blue-500 text-white p-2 rounded-r hover:bg-blue-600 disabled:bg-blue-300"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  )
}