import React, { useEffect, useRef } from 'react'
import { View, Text, Animated, StyleSheet } from 'react-native'
import { theme } from '../constants/theme'

export function TypingIndicator() {
  const dots = [
    useRef(new Animated.Value(0)).current,
    useRef(new Animated.Value(0)).current,
    useRef(new Animated.Value(0)).current,
  ]

  useEffect(() => {
    const animations = dots.map((dot, i) =>
      Animated.loop(
        Animated.sequence([
          Animated.delay(i * 140),
          Animated.timing(dot, { toValue: -5, duration: 300, useNativeDriver: true }),
          Animated.timing(dot, { toValue: 0,  duration: 300, useNativeDriver: true }),
          Animated.delay(220),
        ])
      )
    )
    animations.forEach(a => a.start())
    return () => animations.forEach(a => a.stop())
  }, [])

  const dotColors = [theme.accent, theme.accentMid, theme.accentPale]

  return (
    <View style={styles.row}>
      <View style={styles.avatar}>
        <Text style={styles.avatarText}>PG</Text>
      </View>
      <View style={styles.bubble}>
        {dots.map((dot, i) => (
          <Animated.View
            key={i}
            style={[styles.dot, { backgroundColor: dotColors[i], transform: [{ translateY: dot }] }]}
          />
        ))}
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    alignItems: 'flex-end',
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
  },
  avatarText: {
    fontSize: 9,
    fontWeight: '500',
    color: '#085041',
  },
  bubble: {
    backgroundColor: theme.botBubble,
    borderRadius: 16,
    borderTopLeftRadius: 4,
    borderLeftWidth: 2.5,
    borderLeftColor: theme.accent,
    borderWidth: 0.5,
    borderColor: theme.border,
    paddingHorizontal: 18,
    paddingVertical: 13,
    flexDirection: 'row',
    gap: 5,
    alignItems: 'center',
  },
  dot: {
    width: 7,
    height: 7,
    borderRadius: 4,
  },
})