import React from 'react'
import { Link } from 'react-router-dom'
export default function NavBar() {
  return (
    <div className='flex flex-row justify-between bg-red-500 p-5 text-white font-bold'>
       <div>Nav Bar</div>
       <div >
        <ul className='flex flex-row gap-3'>
            <li><Link to={'/'}>Home</Link> </li>
            <li><Link to={'/about'}>About</Link> </li>
            <li><Link to={'/contact'}>Contact</Link> </li>
            <li><Link to={'/login'}>Login</Link> </li>
        </ul>

       </div>
    </div>
  )
}