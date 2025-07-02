"use client"

import { useState } from "react"
import { signIn } from "next-auth/react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  const handleEmail = async (e: React.FormEvent) => {
    e.preventDefault()
    const res = await signIn("email-login", {
      redirect: false,
      email,
      password,
    })
    if (res?.error) setError("Invalid credentials")
  }

  const handlePhone = async (e: React.FormEvent) => {
    e.preventDefault()
    const res = await signIn("phone-login", {
      redirect: false,
      phone,
      password,
    })
    if (res?.error) setError("Invalid credentials")
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="w-full max-w-sm space-y-6 p-4">
        <form onSubmit={handleEmail} className="space-y-4">
          <Input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button type="submit" className="w-full">
            Login with Email
          </Button>
        </form>
        <form onSubmit={handlePhone} className="space-y-4">
          <Input
            placeholder="Phone"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button type="submit" className="w-full">
            Login with Phone
          </Button>
        </form>
        <Button className="w-full" onClick={() => signIn("google")}>Google Login</Button>
        {error && <p className="text-red-500">{error}</p>}
      </div>
    </div>
  )
}
