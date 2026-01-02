export default function AppLayout({ children }) {
  return (
    <div className="h-screen w-screen flex flex-col bg-gray-50 overflow-hidden">
      {children}
    </div>
  );
}