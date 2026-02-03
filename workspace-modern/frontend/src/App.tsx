import { useEffect } from 'react'
import { WorkspaceHeader } from './components/WorkspaceHeader'
import { NavigationPanel } from './components/NavigationPanel'
import { WorkArea } from './components/WorkArea'
import { ChatPanel } from './components/ChatPanel'
import { PiliProvider } from './context/PiliContext'
import { useWorkspaceStore } from './store/useWorkspaceStore'

function App() {
  const { theme, fetchProjects, fetchQuotes } = useWorkspaceStore()

  // Data Initialization
  useEffect(() => {
    fetchProjects()
    fetchQuotes()
  }, [])

  // Theme Synchronization
  useEffect(() => {
    const root = document.documentElement
    root.classList.remove('light', 'dark', 'magenta')
    root.classList.add(theme)
  }, [theme])

  return (
    <PiliProvider>
      <div className="h-screen flex flex-col bg-white dark:bg-gray-950 transition-colors duration-300">
        <WorkspaceHeader />

        <div className="flex-1 flex overflow-hidden">
          <NavigationPanel />
          <WorkArea />
          <ChatPanel />
        </div>
      </div>
    </PiliProvider>
  )
}

export default App

