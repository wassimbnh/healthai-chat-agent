import { useCallback, useEffect, useRef, useState } from 'react'
import { WS_URL, SESSION_ID } from '../constants/theme'
import { Message, WsStatus } from '../types'

interface UseWebSocketProps {
  onMessage:  (msg: Message) => void
  onTyping:   (typing: boolean) => void
}

export function useWebSocket({ onMessage, onTyping }: UseWebSocketProps) {
  const ws              = useRef<WebSocket | null>(null)
  const reconnectTimer  = useRef<ReturnType<typeof setTimeout> | null>(null)
  const [status, setStatus] = useState<WsStatus>('connecting')

  const connect = useCallback(() => {
    setStatus('connecting')
    const socket = new WebSocket(`${WS_URL}/ws/chat/${SESSION_ID}`)
    ws.current = socket

    socket.onopen = () => setStatus('connected')

    socket.onmessage = (event) => {
      const parsed = JSON.parse(event.data)

      if (parsed.type === 'typing') {
        onTyping(true)
        return
      }
      if (parsed.type === 'message') {
        onTyping(false)
        onMessage(parsed.data as Message)
        return
      }

      // Backend currently sends plain websocket payloads:
      // { message: string, message_id: string }
      // Normalize them to the Message shape expected by the UI.
      if (typeof parsed.message === 'string') {
        onTyping(false)
        onMessage({
          id: parsed.message_id ?? `ws-${Date.now()}`,
          session_id: SESSION_ID,
          role: 'bot',
          content: parsed.message,
          created_at: new Date().toISOString(),
        })
      }
    }

    socket.onclose = () => {
      setStatus('disconnected')
      reconnectTimer.current = setTimeout(connect, 3000)
    }

    socket.onerror = () => {
      socket.close()
    }
  }, [onMessage, onTyping])

  useEffect(() => {
    connect()
    return () => {
      reconnectTimer.current && clearTimeout(reconnectTimer.current)
      ws.current?.close()
    }
  }, [connect])

  const sendMessage = useCallback((content: string) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ message: content }))
    }
  }, [])

  return { status, sendMessage }
}