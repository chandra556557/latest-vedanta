import React, { useEffect, useRef, useState } from 'react';
import { Bot, Send, X } from 'lucide-react';
import { sendFitnessMessage } from '../services/fitnessService';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  options?: string[];
}

const FitnessAssistantWidget: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const ensureGreeted = () => {
    if (messages.length === 0) {
      setMessages([{
        id: Date.now(),
        text: "Hi! I'm the Vedanta Fitness Assistant. Ask me about workouts, diet, or routines.",
        sender: 'bot'
      }]);
    }
  };

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

  const onSubmit = async (e: React.FormEvent) => { e.preventDefault(); const t = input; setInput(''); await send(t); };
  const onOption = async (o: string) => { await send(o); };

  return (
    <>
      {/* Launcher */}
      {!open && (
        <button
          onClick={() => { setOpen(true); setTimeout(ensureGreeted, 0); }}
          className="fixed bottom-24 right-4 z-50 bg-emerald-600 hover:bg-emerald-700 text-white p-4 rounded-full shadow-lg"
          aria-label="Open Vedanta Fitness Assistant"
        >
          <Bot className="w-6 h-6" />
        </button>
      )}

      {/* Widget */}
      {open && (
        <div className="fixed bottom-4 right-4 z-50 w-96 bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden flex flex-col">
          <div className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white p-3 flex items-center justify-between">
            <div className="flex items-center gap-2"><Bot className="w-5 h-5" /><span className="font-semibold">Vedanta Fitness Assistant</span></div>
            <button onClick={() => setOpen(false)} className="p-1 hover:bg-white/10 rounded-full" aria-label="Close">
              <X className="w-5 h-5" />
            </button>
          </div>
          <div className="h-96 overflow-y-auto p-3 bg-gray-50 space-y-3">
            {messages.map(m => (
              <div key={m.id} className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] px-3 py-2 rounded-2xl text-sm ${m.sender === 'user' ? 'bg-emerald-600 text-white' : 'bg-white border border-gray-200 text-gray-800'}`}>
                  <div className="whitespace-pre-wrap">{m.text}</div>
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
          <form onSubmit={onSubmit} className="p-3 border-t bg-white">
            <div className="flex gap-2">
              <input value={input} onChange={e => setInput(e.target.value)} placeholder="Ask about workouts or diet..." className="flex-1 border border-gray-300 rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
              <button type="submit" className="bg-emerald-600 hover:bg-emerald-700 text-white rounded-full px-4">
                <Send className="w-5 h-5" />
              </button>
            </div>
          </form>
        </div>
      )}
    </>
  );
};

export default FitnessAssistantWidget;