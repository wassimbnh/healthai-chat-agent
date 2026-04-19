import React, { useCallback, useRef, useState } from 'react'
import {
  View, Text, TextInput, TouchableOpacity,
  FlatList, KeyboardAvoidingView, Platform,
  StyleSheet, SafeAreaView, Keyboard,
} from 'react-native'
import { useSafeAreaInsets } from 'react-native-safe-area-context'
import { Message } from '../types'
import { theme, SESSION_ID } from '../constants/theme'
import { useMessages } from '../hooks/useMessages'
import { useWebSocket } from '../hooks/useWebSocket'
import { MessageBubble } from '../components/MessageBubble'
import { TypingIndicator } from '../components/TypingIndicator'
import { ConnectionBadge } from '../components/ConnectionBadge'

export default function ChatScreen() {
  const flatListRef        = useRef<FlatList>(null)
  const [input, setInput]  = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [showScrollToBottom, setShowScrollToBottom] = useState(false)
  const insets = useSafeAreaInsets()
  const scrollThreshold = 360 // roughly 5 chat rows

  const { messages, setMessages, loading } = useMessages()

  const handleMessage = useCallback((msg: Message) => {
    setIsTyping(false)
    setMessages(prev => [...prev, msg])
    setTimeout(() => flatListRef.current?.scrollToEnd({ animated: true }), 100)
  }, [])

  const handleTyping = useCallback((typing: boolean) => {
    setIsTyping(typing)
    if (typing) setTimeout(() => flatListRef.current?.scrollToEnd({ animated: true }), 100)
  }, [])

  const { status, sendMessage } = useWebSocket({
    onMessage: handleMessage,
    onTyping:  handleTyping,
  })

  const handleSend = () => {
    const text = input.trim()
    if (!text || status !== 'connected') return

    const optimistic: Message = {
      id:         `temp-${Date.now()}`,
      session_id: SESSION_ID,
      role:       'user',
      content:    text,
      created_at: new Date().toISOString(),
    }

    setMessages(prev => [...prev, optimistic])
    sendMessage(text)
    setIsTyping(true)
    setInput('')
    Keyboard.dismiss()
    setTimeout(() => flatListRef.current?.scrollToEnd({ animated: true }), 100)
  }

  const handleScroll = useCallback((event: any) => {
    const { contentOffset, contentSize, layoutMeasurement } = event.nativeEvent
    const distanceFromBottom = contentSize.height - (contentOffset.y + layoutMeasurement.height)
    setShowScrollToBottom(distanceFromBottom > scrollThreshold)
  }, [])

  const scrollToLatest = useCallback(() => {
    flatListRef.current?.scrollToEnd({ animated: true })
    setShowScrollToBottom(false)
  }, [])

  return (
    <SafeAreaView style={styles.safe}>
      {/* header */}
      <View style={styles.header}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>PG</Text>
        </View>
        <View>
          <Text style={styles.headerName}>Prof. Guttenberg</Text>
          <Text style={styles.headerSub}>Online · Crohn's specialist</Text>
        </View>
      </View>

      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? insets.top : 0}
      >
        {/* messages */}
        <FlatList
          ref={flatListRef}
          data={messages}
          keyExtractor={(m, index) => m.id ?? `${m.created_at}-${index}`}
          renderItem={({ item }) => <MessageBubble message={item} />}
          ListFooterComponent={isTyping ? <TypingIndicator /> : null}
          contentContainerStyle={[styles.list, { paddingBottom: 8 }]}
          keyboardShouldPersistTaps="handled"
          keyboardDismissMode="interactive"
          onScroll={handleScroll}
          scrollEventThrottle={16}
          onContentSizeChange={() => {
            if (!showScrollToBottom) {
              flatListRef.current?.scrollToEnd({ animated: false })
            }
          }}
        />
        {showScrollToBottom ? (
          <TouchableOpacity
            style={[styles.scrollToBottomBtn, { bottom: 84 + insets.bottom }]}
            onPress={scrollToLatest}
            activeOpacity={0.85}
          >
            <Text style={styles.scrollToBottomIcon}>↓</Text>
          </TouchableOpacity>
        ) : null}

        {/* status + input */}
        <ConnectionBadge status={status} />
        <View style={[styles.inputRow, { paddingBottom: 10 + Math.max(insets.bottom, 0) }]}>
          <TextInput
            style={styles.input}
            value={input}
            onChangeText={setInput}
            placeholder="Ask the professor..."
            placeholderTextColor={theme.accentMid}
            onSubmitEditing={handleSend}
            returnKeyType="send"
            multiline
            scrollEnabled
            blurOnSubmit
            enablesReturnKeyAutomatically
          />
          <TouchableOpacity
            style={[styles.sendBtn, status !== 'connected' && { opacity: 0.4 }]}
            onPress={handleSend}
            disabled={status !== 'connected'}
          >
            <Text style={styles.sendIcon}>↑</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  )
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: theme.bg,
  },
  header: {
    backgroundColor: theme.headerBg,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    paddingHorizontal: 20,
    paddingVertical: 14,
  },
  avatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#E1F5EE',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: 'rgba(255,255,255,0.5)',
  },
  avatarText: {
    fontSize: 12,
    fontWeight: '500',
    color: '#0F6E56',
  },
  headerName: {
    fontSize: 14,
    fontWeight: '500',
    color: '#04342C',
  },
  headerSub: {
    fontSize: 11,
    color: '#085041',
    marginTop: 2,
  },
  list: {
    paddingHorizontal: 14,
    paddingTop: 12,
    paddingBottom: 8,
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    backgroundColor: theme.bg,
    borderTopWidth: 0.5,
    borderTopColor: 'rgba(93,202,165,0.15)',
  },
  input: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 22,
    borderWidth: 0.5,
    borderColor: theme.border,
    paddingHorizontal: 16,
    paddingTop: 10,
    paddingBottom: 10,
    fontSize: 13,
    color: theme.botText,
    minHeight: 42,
    maxHeight: 100,
    textAlignVertical: 'top',
    overflow: 'hidden',
  },
  sendBtn: {
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: theme.accent,
    alignItems: 'center',
    justifyContent: 'center',
  },
  sendIcon: {
    fontSize: 18,
    color: '#fff',
    fontWeight: '500',
  },
  scrollToBottomBtn: {
    position: 'absolute',
    right: 16,
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: theme.accent,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.12,
    shadowRadius: 4,
    shadowOffset: { width: 0, height: 2 },
    elevation: 3,
  },
  scrollToBottomIcon: {
    fontSize: 20,
    color: '#fff',
    fontWeight: '600',
  },
})