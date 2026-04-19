export type MessageRole = 'user' | 'bot'

export interface Message {
  id: string
  session_id?: string
  role: MessageRole
  content: string
  created_at: string
}

export type WsStatus = 'connecting' | 'connected' | 'disconnected'

export type WsEventType = 'typing' | 'message' | 'error'

export interface WsEvent {
  type: WsEventType
  data?: Message
  error?: string
}