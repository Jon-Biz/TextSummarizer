import React, { useState } from 'react'
import { Settings } from '../types'

interface SettingsModalProps {
  settings: Settings | null
  onClose: () => void
  onSettingsChange: (settings: Settings) => void
}

const SettingsModal: React.FC<SettingsModalProps> = ({
  settings,
  onClose,
  onSettingsChange,
}) => {
  const [systemPrompt, setSystemPrompt] = useState(settings?.systemPrompt || '')
  const [openaiApiKey, setOpenaiApiKey] = useState(settings?.openaiApiKey || '')
  const [openaiEndpoint, setOpenaiEndpoint] = useState(
    settings?.openaiEndpoint || ''
  )

  const handleSave = () => {
    const newSettings: Settings = {
      systemPrompt,
      openaiApiKey,
      openaiEndpoint,
    }
    onSettingsChange(newSettings)
    onClose()
  }

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-8 rounded-lg">
        <h2 className="text-2xl font-bold mb-4">Settings</h2>
        <div className="mb-4">
          <label htmlFor="systemPrompt" className="block font-bold mb-2">
            System Prompt
          </label>
          <textarea
            id="systemPrompt"
            value={systemPrompt}
            onChange={(e) => setSystemPrompt(e.target.value)}
            className="w-full border border-gray-300 rounded-md p-2"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="openaiApiKey" className="block font-bold mb-2">
            OpenAI API Key
          </label>
          <input
            id="openaiApiKey"
            type="text"
            value={openaiApiKey}
            onChange={(e) => setOpenaiApiKey(e.target.value)}
            className="w-full border border-gray-300 rounded-md p-2"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="openaiEndpoint" className="block font-bold mb-2">
            OpenAI Endpoint
          </label>
          <input
            id="openaiEndpoint"
            type="text"
            value={openaiEndpoint}
            onChange={(e) => setOpenaiEndpoint(e.target.value)}
            className="w-full border border-gray-300 rounded-md p-2"
          />
        </div>
        <div className="flex justify-end">
          <button
            onClick={handleSave}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  )
}

export default SettingsModal