import React, { useState } from 'react';
import axios from 'axios';
import Link from 'next/link';
import { useRouter } from 'next/router';


function Login() {
  const router = useRouter();
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';

  const [credentials, setCredentials] = useState({ email: '', password: '' });

  // Create user
  const handleSignin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevent default form submission
    try {
      const response = await axios.post(`${apiUrl}/api/flask/login`, credentials);
      setCredentials({ email: '', password: '' });
      console.log("Successfully logged in", response.data);
      router.push("/home")
    } catch (error) {
      console.error('Error creating user:', error);
    }
  }; 
  return (
    <main className="flex flex-col items-center justify-center w-full flex-1 px-20 py-60 text-center">
      <div className="bg-white rounded-2xl shadow-2xl flex w-2/3 max-w-4xl">
        <div className="w-3/5 p-5">
          <div className="text-left font-bold">
            <span className="text-blue-700"> Company</span> Name
          </div>
          <div className="py-10">
            <h2 className="text-3xl font-bold text-blue-700 mb-2">Sign into account</h2>
            <div className="border-2 w-10 border-blue-700 inline-block mb-2"></div>
            <p>Log in into your account</p>
            <div className="flex flex-col items-center">
              <form onSubmit={handleSignin} className="mb-6 p-4 bg-blue-100 rounded shadow">
                <input
                  name="email"
                  placeholder="Email"
                  value={credentials.email}
                  onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
                  className="mb-2 w-full p-2 border border-gray-300 rounded"
                />
                <input
                  name="password"
                  type="password"
                  placeholder="Password"
                  value={credentials.password}
                  onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                  className="mb-2 w-full p-2 border border-gray-300 rounded"
                />
                <button type="submit" className="w-full p-2 text-white bg-blue-500 rounded hover:bg-blue-600">
                  Sign in
                </button>
              </form>
            </div>
          </div>
        </div>
        {/* sign in section */}
        <div className="w-2/5 bg-blue-500 text-white rounded-tr-2xl rounded-br-2xl py-36 px-12">
          <h2 className="text-3xl font-bold mb-2">Hello, Friend</h2>
          <div className="border-2 w-10 border-white inline-block mb-2"></div>
          <p className="mb-10">Fill up personal information.</p>
          <Link href={"/signup"}><a className="border-2 border-white rounded-full px-12 py-2 inline-block font-semibold hover:bg-white hover:text-blue-700">Sign Up</a></Link>
        </div>
      </div>
    </main>
  );
}


export default Login;