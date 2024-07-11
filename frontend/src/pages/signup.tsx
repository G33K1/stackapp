import React, { useState } from 'react';
import axios from 'axios';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { METHODS } from 'http';

 

function Signup() {
  const router = useRouter();
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';

  const [credentials, setCredentials] = useState({ username: '', email: '', password: '', password2: '' });

// Create user
  const handleSignup = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(credentials)
    console.log({credentials})
    console.log(JSON.stringify(credentials))

    try {
      console.log("Awaiting logs");
      // const response = await fetch(`${apiUrl}/api/flask/signup`,{
      //   method: "POST",
      //   body: JSON.stringify(credentials)
      // });
      let headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
      const response = await axios.post(`${apiUrl}/api/flask/signup`, { data: credentials, config: headers});
      console.log(response)
      if (response.status == 200) {
        setCredentials({ username: '', email: '', password: '' , password2: '' });
        console.log("Successfully logged in", response);
        router.push("/home")
      }
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
            <h2 className="text-3xl font-bold text-blue-700 mb-2">Create an account</h2>
            <div className="border-2 w-10 border-blue-700 inline-block mb-2"></div>
            <p>Sign up</p>
            <form onSubmit={handleSignup} className="mb-6 p-4 bg-blue-100 rounded shadow">
            <input
                  name="username"
                  placeholder="username"
                  value={credentials.username}
                  onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
                  className="mb-2 w-full p-2 border border-gray-300 rounded"
                />
                <input
                  name="email"
                  placeholder="Email"
                  value={credentials.email}
                  onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
                  className="mb-2 w-full p-2 border border-gray-300 rounded"
                />
                <input
                  name="password"
                  placeholder="Password"
                  value={credentials.password}
                  onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                  className="mb-2 w-full p-2 border border-gray-300 rounded"
                />
                <input
                  name="password2"
                  placeholder="password2"
                  value={credentials.password2}
                  onChange={(e) => setCredentials({ ...credentials, password2: e.target.value })}
                  className="mb-2 w-full p-2 border border-gray-300 rounded"
                />
                <button type="submit" className="w-full p-2 text-white bg-blue-500 rounded hover:bg-blue-600">
                  Sign Up
                </button>
              </form>
          </div>
        </div>
        {/* sign in section */}
      </div>
    </main>
  );
}

export default Signup;