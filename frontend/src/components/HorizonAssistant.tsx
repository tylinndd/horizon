import { useState, useRef, useEffect } from 'react'
import { queryLLM } from '../services/api'
import './HorizonAssistant.css'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function HorizonAssistant() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hello! I\'m the Horizon Assistant. I can help you understand risk scores, explain anomalies, and answer questions about outbreak detection. How can I help you today?'
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage: Message = { role: 'user', content: input }
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await queryLLM(input)
      const assistantMessage: Message = { role: 'assistant', content: response.response }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error querying LLM:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again later.'
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="horizon-assistant">
      <div className="assistant-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message message-${msg.role}`}>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}
        {loading && (
          <div className="message message-assistant">
            <div className="message-content">Thinking...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form className="assistant-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about outbreak risks, anomalies, or health metrics..."
          className="assistant-input"
          disabled={loading}
        />
        <button type="submit" className="assistant-submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  )
}

