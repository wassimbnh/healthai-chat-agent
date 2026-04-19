import React from 'react'
import { View, Text, StyleSheet } from 'react-native'
import { Message } from '../types'
import { theme } from '../constants/theme'

interface Props {
  message: Message
}

export function MessageBubble({ message }: Props) {
  const isUser = message.role === 'user'
  const time   = new Date(message.created_at).toLocaleTimeString([], {
    hour: '2-digit', minute: '2-digit'
  })

  if (isUser) {
    return (
      <View style={styles.userRow}>
        <View style={styles.userBubble}>
          <Text style={styles.userText}>{message.content}</Text>
        </View>
        <Text style={styles.timestamp}>{time}</Text>
      </View>
    )
  }

  return (
    <View style={styles.botRow}>
      <View style={styles.avatar}>
        <Text style={styles.avatarText}>PG</Text>
      </View>
      <View>
        <View style={styles.botBubble}>
          <Text style={styles.botText}>{message.content}</Text>
        </View>
        <Text style={styles.timestamp}>{time}</Text>
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  userRow: {
    width: '100%',
    alignItems: 'flex-end',
    marginBottom: 12,
  },
  userBubble: {
    backgroundColor: theme.userBubble,
    borderRadius: 16,
    borderTopRightRadius: 4,
    paddingHorizontal: 14,
    paddingVertical: 10,
    maxWidth: '78%',
  },
  userText: {
    color: theme.userText,
    fontSize: 13,
    lineHeight: 20,
  },
  botRow: {
    width: '100%',
    flexDirection: 'row',
    alignItems: 'flex-end',
    justifyContent: 'flex-start',
    gap: 8,
    marginBottom: 12,
  },
  avatar: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: theme.accentMid,
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0,
  },
  avatarText: {
    fontSize: 9,
    fontWeight: '500',
    color: '#085041',
  },
  botBubble: {
    backgroundColor: theme.botBubble,
    borderRadius: 16,
    borderTopLeftRadius: 4,
    borderLeftWidth: 2.5,
    borderLeftColor: theme.accent,
    borderWidth: 0.5,
    borderColor: theme.border,
    paddingHorizontal: 14,
    paddingVertical: 10,
    maxWidth: '84%',
  },
  botText: {
    color: theme.botText,
    fontSize: 13,
    lineHeight: 20,
  },
  timestamp: {
    fontSize: 10,
    color: theme.muted,
    marginTop: 3,
    paddingHorizontal: 4,
  },
})