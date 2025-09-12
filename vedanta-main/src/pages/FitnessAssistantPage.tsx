import React, { useEffect, useRef, useState } from 'react';
import { Send, Bot, X } from 'lucide-react';
import { sendFitnessMessage } from '../services/fitnessService';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  options?: string[];
}

const FitnessAssistantPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([{
    id: 1,
    text: "Hi! I'm the Vedanta Fitness Assistant. Ask me about workouts, diet plans, or routines.",
    sender: 'bot'
  }]);
  const [input, setInput] = useState('');
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const send = async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed) return;
    const userMsg: Message = { id: Date.now(), text: trimmed, sender: 'user' };
    setMessages(prev => [...prev, userMsg]);

    try {
      const res = await sendFitnessMessage(trimmed);
      const botMsg: Message = { id: Date.now() + 1, text: res.response, sender: 'bot', options: res.options };
      setMessages(prev => [...prev, botMsg]);
    } catch (e) {
      setMessages(prev => [...prev, { id: Date.now() + 2, text: 'Sorry, something went wrong.', sender: 'bot' }]);
    }
  };

  const onSubmit = async (e: React.FormEvent) => { e.preventDefault(); const current = input; setInput(''); await send(current); };

  const onOption = async (opt: string) => { await send(opt); };

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-3xl mx-auto p-4">
        <div className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white p-4 rounded-t-2xl flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Bot className="w-6 h-6" />
            <h1 className="text-lg font-semibold">Vedanta Fitness Assistant</h1>
          </div>
        </div>
        <div className="border border-gray-200 rounded-b-2xl overflow-hidden">
          <div className="h-[60vh] overflow-y-auto p-4 space-y-4 bg-gray-50">
            {messages.map(m => (
              <div key={m.id} className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] px-4 py-2 rounded-2xl ${m.sender === 'user' ? 'bg-emerald-600 text-white' : 'bg-white text-gray-800 border border-gray-200'}`}>
                  <div className="whitespace-pre-wrap text-sm">{m.text}</div>
                  {m.options && m.options.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {m.options.map((o, i) => (
                        <button key={i} onClick={() => onOption(o)} className="bg-white text-gray-700 border border-gray-300 rounded-full px-3 py-1 text-xs hover:bg-gray-100">
                          {o}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            <div ref={endRef} />
          </div>
          <form onSubmit={onSubmit} className="p-4 bg-white border-t border-gray-200">
            <div className="flex gap-2">
              <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask about workouts or diet..." className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500" />
              <button type="submit" className="bg-emerald-600 text-white rounded-full p-2 px-4 hover:bg-emerald-700">
                <Send className="w-5 h-5" />
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default FitnessAssistantPage;