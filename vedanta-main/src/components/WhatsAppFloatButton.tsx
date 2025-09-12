import React from "react";

const WHATSAPP_INTL_NUMBER = "14155550123"; // Replace with your number (country code + number, no '+')
const DEFAULT_TEXT = "Hi! I need help with my health/fitness plan.";

export const WhatsAppFloatButton: React.FC = () => {
  const href = `https://wa.me/${WHATSAPP_INTL_NUMBER}?text=${encodeURIComponent(DEFAULT_TEXT)}`;

  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      aria-label="Chat on WhatsApp"
      className="fixed bottom-6 right-6 z-50 bg-[#25D366] text-white rounded-full px-4 py-3 shadow-lg font-semibold hover:bg-green-500 focus:outline-none focus:ring-2 focus:ring-green-300"
    >
      Chat on WhatsApp
    </a>
  );
};

export default WhatsAppFloatButton;
