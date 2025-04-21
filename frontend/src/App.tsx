import React from 'react';
import './App.css';
import { useState, useEffect, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';
import { format } from 'date-fns';

interface Bookmark {
  title: string;
  url: string;
  remember_date: string;
}

interface FormState {
  title: string;
  url: string;
  remember_date: string;
}

function App() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [form, setForm] = useState<FormState>({
    title: '',
    url: '',
    remember_date: ''
  });

  useEffect(() => {
    fetchBookmarks();
  }, []);

  const fetchBookmarks = async () => {
    const res = await axios.get<Bookmark[]>('http://localhost:5000/bookmarks');
    const sorted = res.data.sort((a, b) => new Date(a.remember_date).getTime() - new Date(b.remember_date).getTime());
    setBookmarks(sorted);
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    await axios.post('http://localhost:5000/bookmarks', form);
    setForm({ title: '', url: '', remember_date: '' });
    fetchBookmarks();
  };

  const isToday = (dateStr: string) => {
    const today = format(new Date(), 'yyyy-MM-dd');
    return today === dateStr;
  };

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Bookmarks</h1>

      <form onSubmit={handleSubmit} className="mb-8 space-y-4">
        <input
          type="text"
          name="title"
          placeholder="Title"
          value={form.title}
          onChange={handleChange}
          className="border p-2 w-full"
          required
        />
        <input
          type="url"
          name="url"
          placeholder="URL"
          value={form.url}
          onChange={handleChange}
          className="border p-2 w-full"
          required
        />
      <label className="block">
        Remember Date
        <input
          className="border p-2 w-full"
          name="remember_date"
          placeholder="Date"   
          required
          type="date"
        />
      </label>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Add Bookmark
        </button>
      </form>

      <ul className="space-y-4">
        {bookmarks.map((bookmark, index) => (
          <li key={index} className={`p-4 border rounded ${isToday(bookmark.remember_date) ? 'bg-yellow-100' : ''}`}>
            <h2 className="text-lg font-semibold">{bookmark.title}</h2>
            <a href={bookmark.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">
              {bookmark.url}
            </a>
            <p className="text-gray-600">Remember Date: {bookmark.remember_date}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
