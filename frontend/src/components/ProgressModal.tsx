import React from 'react'

const ProgressModal: React.FC = () => {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-8 rounded-lg">
        <h2 className="text-2xl font-bold mb-4">Processing...</h2>
        <p>Please wait while we process your audio file.</p>
      </div>
    </div>
  )
}

export default ProgressModal