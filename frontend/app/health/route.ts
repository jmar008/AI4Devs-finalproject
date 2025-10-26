import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json(
    {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'dealaai-frontend',
      version: '1.0.0',
      environment: process.env.NODE_ENV || 'development',
    },
    { status: 200 }
  )
}