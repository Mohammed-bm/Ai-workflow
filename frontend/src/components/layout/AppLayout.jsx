export default function AppLayout({ children }) {
  return (
    <div className="h-screen w-screen flex flex-col bg-gray-950 text-white">
      {children}
    </div>
  );
}
    