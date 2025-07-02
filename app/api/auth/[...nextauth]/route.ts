import NextAuth from "next-auth"
import type { NextAuthOptions } from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials"
import GoogleProvider from "next-auth/providers/google"
import bcrypt from "bcryptjs"

const users = [
  {
    id: "1",
    email: "demo@example.com",
    phone: "1234567890",
    passwordHash: bcrypt.hashSync("password", 10),
  },
]

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      id: "email-login",
      name: "Email",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        const user = users.find((u) => u.email === credentials?.email)
        if (user && credentials?.password &&
            (await bcrypt.compare(credentials.password, user.passwordHash))) {
          return { id: user.id, email: user.email }
        }
        return null
      },
    }),
    CredentialsProvider({
      id: "phone-login",
      name: "Phone",
      credentials: {
        phone: { label: "Phone", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        const user = users.find((u) => u.phone === credentials?.phone)
        if (user && credentials?.password &&
            (await bcrypt.compare(credentials.password, user.passwordHash))) {
          return { id: user.id, phone: user.phone }
        }
        return null
      },
    }),
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID ?? "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? "",
    }),
  ],
  session: { strategy: "jwt" },
  secret: process.env.NEXTAUTH_SECRET,
}

const handler = NextAuth(authOptions)
export { handler as GET, handler as POST }
