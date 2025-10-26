import { cn } from '@/lib/utils'
import * as React from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?:
    | 'default'
    | 'destructive'
    | 'outline'
    | 'secondary'
    | 'ghost'
    | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'default', ...props }, ref) => {
    return (
      <button
        className={cn(
          'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
          {
            'bg-indigo-600 text-white hover:bg-indigo-700 focus:ring-indigo-500':
              variant === 'default',
            'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500':
              variant === 'destructive',
            'border border-gray-300 bg-white hover:bg-gray-50 focus:ring-indigo-500':
              variant === 'outline',
            'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-400':
              variant === 'secondary',
            'hover:bg-gray-100 focus:ring-gray-400': variant === 'ghost',
            'text-indigo-600 underline-offset-4 hover:underline focus:ring-indigo-500':
              variant === 'link',
          },
          {
            'h-10 px-4 py-2': size === 'default',
            'h-9 rounded-md px-3': size === 'sm',
            'h-11 rounded-md px-8': size === 'lg',
            'h-10 w-10': size === 'icon',
          },
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = 'Button'

export { Button }
