import React from 'react'
import { View, Text, StyleSheet } from 'react-native'
import { WsStatus } from '../types'

const config: Record<WsStatus, { bg: string; dot: string; text: string; label: string }> = {
  connected:    { bg: '#E1F5EE', dot: '#5DCAA5', text: '#0F6E56', label: '' },
  connecting:   { bg: '#FAEEDA', dot: '#EF9F27', text: '#854F0B', label: 'Trying to reconnect...' },
  disconnected: { bg: '#FAECE7', dot: '#D85A30', text: '#993C1D', label: 'Connection lost. Trying again...' },
}

export function ConnectionBadge({ status }: { status: WsStatus }) {
  if (status === 'connected') return null
  const c = config[status]
  return (
    <View style={[styles.bar, { backgroundColor: c.bg }]}>
      <View style={[styles.dot, { backgroundColor: c.dot }]} />
      <Text style={[styles.label, { color: c.text }]}>{c.label}</Text>
    </View>
  )
}

const styles = StyleSheet.create({
  bar: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingVertical: 6,
    paddingHorizontal: 16,
    borderTopWidth: 0.5,
    borderTopColor: 'rgba(93,202,165,0.2)',
  },
  dot: {
    width: 6,
    height: 6,
    borderRadius: 3,
  },
  label: {
    fontSize: 10,
    fontWeight: '500',
    letterSpacing: 0.3,
  },
})