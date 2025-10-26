'use client'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useState } from 'react'

export default function TestInputsPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold">Test Inputs</h1>
          <p className="text-sm text-gray-600">Prueba de componentes UI</p>
        </div>

        <div className="space-y-4 rounded-lg bg-white p-8 shadow">
          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700">
              Username
            </label>
            <Input
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <p className="mt-1 text-xs text-gray-500">Value: {username}</p>
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700">
              Password
            </label>
            <Input
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <p className="mt-1 text-xs text-gray-500">Value: {password}</p>
          </div>

          <div className="pt-4">
            <Button
              onClick={() => {
                console.log('Username:', username)
                console.log('Password:', password)
                alert(`Username: ${username}\nPassword: ${password}`)
              }}
              className="w-full"
            >
              Test Button
            </Button>
          </div>

          <div className="border-t pt-4">
            <p className="text-xs text-gray-600">
              Si puedes escribir en los inputs y hacer click en el botón, todo
              funciona correctamente.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
