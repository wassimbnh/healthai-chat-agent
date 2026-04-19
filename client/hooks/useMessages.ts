import { useEffect, useState } from 'react'
import { API_URL, SESSION_ID } from '../constants/theme'
import { Message } from '../types'

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
        setMessages(normalized)
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return { messages, setMessages, loading, error }
}