"use client";

import { useState } from "react";
import Image from "next/image";

interface MovieResult {
  title: string;
  release_date: string;
  genres: string[];
  score: number;
  overview: string;
  poster_path: string | null;
}

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<MovieResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setHasSearched(true);
    
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
      const data = await res.json();
      setResults(data.results || []);
    } catch (error) {
      console.error("Search failed:", error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-6 md:p-12 lg:p-24 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-[#0f172a] to-black">
      <div className="max-w-5xl mx-auto flex flex-col items-center">
        {/* Header */}
        <div className={`transition-all duration-500 ease-out flex flex-col items-center w-full ${hasSearched ? 'mt-4 mb-8' : 'mt-[20vh] mb-12'}`}>
          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500 animate-slide-up mb-4">
            MovieSearch
          </h1>
          <p className="text-slate-400 text-lg md:text-xl text-center max-w-2xl animate-fade-in" style={{animationDelay: '0.1s'}}>
            Khám phá thế giới điện ảnh với hệ thống tìm kiếm thông minh.
          </p>
        </div>

        {/* Search Bar */}
        <div className="w-full max-w-3xl animate-slide-up" style={{animationDelay: '0.2s'}}>
          <form onSubmit={handleSearch} className="relative group">
            <div className="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
              <svg className="w-5 h-5 text-slate-400 group-focus-within:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
            <input 
              type="text" 
              className="w-full bg-slate-900/50 border border-slate-700/50 text-white text-lg rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block pl-12 p-4 transition-all glass backdrop-blur-xl outline-none placeholder:text-slate-500"
              placeholder="Nhập tên phim, diễn viên, thể loại..." 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button 
              type="submit" 
              disabled={loading}
              className="text-white absolute right-2.5 bottom-2.5 bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-xl text-sm px-6 py-2.5 transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {loading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Đang tìm...
                </>
              ) : (
                'Tìm kiếm'
              )}
            </button>
          </form>
        </div>

        {/* Results */}
        {hasSearched && (
          <div className="w-full mt-12 animate-fade-in">
            {!loading && (
              <div className="mb-6 flex justify-between items-end">
                <h2 className="text-2xl font-bold text-white">Kết quả tìm kiếm</h2>
                <span className="text-slate-400 bg-slate-800/50 px-3 py-1 rounded-full text-sm">
                  {results.length} bộ phim
                </span>
              </div>
            )}
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {results.map((movie, idx) => (
                <div 
                  key={idx} 
                  className="glass glass-hover rounded-2xl overflow-hidden flex flex-row animate-slide-up h-[200px]"
                  style={{ animationDelay: `${0.05 * Math.min(idx, 10)}s` }}
                >
                  <div className="w-[133px] relative bg-slate-800 flex-shrink-0 h-full">
                    {movie.poster_path ? (
                      <Image 
                        src={`https://image.tmdb.org/t/p/w342${movie.poster_path}`} 
                        alt={movie.title}
                        fill
                        className="object-cover"
                        sizes="133px"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-slate-600">
                        <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                        </svg>
                      </div>
                    )}
                    <div className="absolute top-2 left-2 bg-black/60 backdrop-blur-md px-2 py-1 rounded-md text-xs font-bold text-yellow-400 border border-yellow-400/20 flex items-center gap-1">
                      <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                      </svg>
                      {movie.score.toFixed(2)}
                    </div>
                  </div>
                  
                  <div className="p-5 flex flex-col justify-start w-full overflow-hidden">
                    <h3 className="text-xl font-bold text-white mb-2 line-clamp-1" title={movie.title}>
                      {movie.title}
                    </h3>
                    
                    <div className="flex flex-wrap items-center gap-2 mb-3 text-xs flex-shrink-0">
                      {movie.release_date && (
                        <span className="text-blue-400 font-medium bg-blue-900/30 px-2 py-0.5 rounded">
                          {movie.release_date.split('-')[0]}
                        </span>
                      )}
                      {movie.genres && movie.genres.length > 0 && (
                        <span className="text-slate-400 truncate">
                          {movie.genres.slice(0, 2).join(', ')}
                          {movie.genres.length > 2 ? ', ...' : ''}
                        </span>
                      )}
                    </div>
                    
                    <p className="text-slate-300 text-sm line-clamp-3 leading-relaxed">
                      {movie.overview || 'Không có mô tả cho bộ phim này.'}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {!loading && results.length === 0 && hasSearched && (
              <div className="text-center py-20 glass rounded-2xl mt-6">
                <svg className="w-16 h-16 text-slate-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <h3 className="text-xl font-semibold text-white mb-2">Không tìm thấy kết quả</h3>
                <p className="text-slate-400">Thử một từ khóa khác hoặc kiểm tra lại chính tả nhé.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
