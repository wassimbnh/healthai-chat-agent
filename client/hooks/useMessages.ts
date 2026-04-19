import { useEffect, useState } from 'react'
import { API_URL, SESSION_ID } from '../constants/theme'
import { Message } from '../types'

const WELCOME_MESSAGE: Message = {
  id: 'welcome-message',
  session_id: SESSION_ID,
  role: 'bot',
  content:
    "Hi, I'm Professor Guttenberg. I can help with Crohn's treatment questions like side effects, missed doses, and day-to-day habits. Share what's on your mind, and we can go step by step.",
  created_at: new Date().toISOString(),
}

export function useMessages() {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState<string | null>(null)

  useEffect(() => {
    fetch(`${API_URL}/api/messages?session_id=${SESSION_ID}`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to load history')
        return res.json()
      })
      .then((data: Array<{
        message_id: string
        session_id?: string
        role: string
        content: string
        created_at: string
      }>) => {
        const normalized: Message[] = data.map((msg) => ({
          id: msg.message_id,
          session_id: msg.session_id,
          role: msg.role.toLowerCase() === 'user' ? 'user' : 'bot',
          content: msg.content,
          created_at: msg.created_at,
        }))
        setMessages(normalized.length > 0 ? normalized : [WELCOME_MESSAGE])
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return { messages, setMessages, loading, error }
}