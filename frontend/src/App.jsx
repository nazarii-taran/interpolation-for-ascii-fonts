import React, { useState, useEffect } from 'react';
import { getAllFonts, getAsciiBlocks } from './api';

export default function App() {
  const [asciiBlocks, setAsciiBlocks] = useState([]);
  const [text, setText] = useState('hello world!');
  const [algorithm, setAlgorithm] = useState('nearest-neighbour');
  const [fonts, setFonts] = useState([]);
  const [currentFont, setCurrentFont] = useState('');
  const [scale, setScale] = useState('1');

  const fetchAllFonts = async () => {
    const fonts = await getAllFonts();
      setFonts(fonts);
      if (fonts && fonts.length) {
        setCurrentFont(fonts[0]);
      }
  };

  const updatedAsciiText = async () => {
    if (scale && currentFont && algorithm) {
      const chars = await getAsciiBlocks(text, scale, currentFont, algorithm);
      setAsciiBlocks(chars);
    }
  };

  const copyToClipboard = () => {
    let copyText = '';
    for (let row = 0; row < asciiBlocks[0].length; row++) {
      for (const block of asciiBlocks) {
        copyText += block[row] + '   ';
      }

      copyText += '\n';
    }

    navigator.clipboard.writeText(copyText);
  }

  useEffect(() => {
    const timer = setTimeout(async () => {
      await updatedAsciiText();
    }, 300);

    return () => clearTimeout(timer);
  }, [text, algorithm, currentFont, scale]);

  useEffect(() => {
    fetchAllFonts();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">
            ASCII fonts & matrix interploation
          </h1>

          <div className="space-y-2">
            <div className="flex space-x-4 items-end">
              {/* Search Input */}
              <div className="flex-grow">
                <label
                  htmlFor="text"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Text
                </label>
                <input
                  type="text"
                  id="text"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Type text to convert to ASCII.."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>

              {/* Interpolation method */}
              <div className="w-40">
                <label
                  htmlFor="algorithm"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Interpolation algorithm
                </label>
                <select
                  id="algorithm"
                  value={algorithm}
                  onChange={(e) => setAlgorithm(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="nearest-neighbour">Nearest neighbour</option>
                  <option value="bilinear">Bilinear</option>
                  <option value="bicubic">Bicubic</option>
                </select>
              </div>

              {/* Font Size Dropdown */}
              <div className="w-20">
                <label
                  htmlFor="fontSize"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Font scale
                </label>
                <select
                  id="fontSize"
                  value={scale}
                  onChange={(e) => setScale(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="1">x1</option>
                  <option value="2">x2</option>
                  <option value="3">x3</option>
                  <option value="5">x5</option>
                  <option value="10">x10</option>
                </select>
              </div>

              {/* Font Type Dropdown */}
              <div className="w-20">
                <label
                  htmlFor="serverFonts"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Font type
                </label>
                <select
                  id="serverFonts"
                  value={currentFont}
                  onChange={(e) => setCurrentFont(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  {fonts.map(f => {
                    return <option key={f} value={f}>{f}</option>
                  })}
                </select>
              </div>
            </div>
          </div>

          {asciiBlocks && asciiBlocks.length > 0 && <div className="flex flex-row flex-wrap justify-center items-center mt-6">
            {asciiBlocks.map(block => block.join('\n')).map((str, index) => (
              <div
                key={index}
                className={`
                    p-4 text-gray-700 flex-grow-0 flex-shrink-0 basis-auto
                    whitespace-pre-wrap font-mono text-custom_tiny leading-none
                  `}
              >
                {str}
              </div>
            ))}
            <div className="copy-btn self-start" onClick={copyToClipboard}>
              <svg className="h-6 w-6"  width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="#000" fill="none" strokeLinecap="round" strokeLinejoin="round">
                <path stroke="none" d="M0 0h24v24H0z"/>
                <rect x="8" y="8" width="12" height="12" rx="2" />
                <path d="M16 8v-2a2 2 0 0 0 -2 -2h-8a2 2 0 0 0 -2 2v8a2 2 0 0 0 2 2h2" />
              </svg>
            </div>
          </div>}
        </div>
      </div>
    </div>
  );
}