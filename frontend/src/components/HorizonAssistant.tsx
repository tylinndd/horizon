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

  const getFallbackResponse = (query: string): string => {
    const lowerQuery = query.toLowerCase()
    
    if (lowerQuery.includes('risk') || lowerQuery.includes('outbreak')) {
      return 'Risk scores are calculated based on multiple factors including pharmacy purchases, search trends, hospital utilization, and anomaly detection. Higher scores indicate increased likelihood of an outbreak.'
    }
    if (lowerQuery.includes('anomaly') || lowerQuery.includes('unusual')) {
      return 'Anomalies are detected when health indicators deviate significantly from normal patterns. These can include spikes in medication purchases, increased search interest in symptoms, or unusual hospital utilization patterns.'
    }
    if (lowerQuery.includes('region') || lowerQuery.includes('location')) {
      return 'Regions are identified by codes like US-CA (California), US-NY (New York), etc. Each region is monitored independently for outbreak risks.'
    }
    if (lowerQuery.includes('critical') || lowerQuery.includes('high risk')) {
      return 'Critical risk levels indicate a very high probability of an outbreak. Immediate action may be required. High risk suggests elevated concern but may not require immediate intervention.'
    }
    if (lowerQuery.includes('help') || lowerQuery.includes('what can')) {
      return 'I can help you understand risk scores, explain anomalies, answer questions about outbreak detection, and provide information about regions and health metrics. What would you like to know?'
    }
    
    return `I understand you're asking about "${query}". To provide more detailed responses, please configure an OpenRouter API key in the backend settings. For now, I can tell you that Horizon monitors health indicators across regions to detect potential outbreaks early. Would you like to know more about risk scoring, anomalies, or specific regions?`
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage: Message = { role: 'user', content: input }
    setMessages((prev) => [...prev, userMessage])
    const userInput = input
    setInput('')
    setLoading(true)

    try {
      const response = await queryLLM(userInput)
      const assistantMessage: Message = { role: 'assistant', content: response.response }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error: any) {
      console.error('Error querying LLM:', error)
      // Use fallback response when API is not available
      const fallbackResponse = getFallbackResponse(userInput)
      const errorMessage: Message = {
        role: 'assistant',
        content: fallbackResponse
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

