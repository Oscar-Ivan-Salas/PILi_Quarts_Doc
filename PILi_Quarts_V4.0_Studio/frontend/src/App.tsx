import { useEffect } from 'react'
import { WorkspaceHeader } from './components/WorkspaceHeader'
import { NavigationPanel } from './components/NavigationPanel'
import { WorkArea } from './components/WorkArea'
import { PiliProvider } from './context/PiliContext'
import { useWorkspaceStore } from './store/useWorkspaceStore'

import { AnimatedAIChat } from './components/ui/AnimatedAIChat'

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
      <div className="h-screen flex flex-col bg-[#030712] transition-colors duration-300 overflow-hidden">
        <WorkspaceHeader />

        {/* MAIN LAYOUT 10-60-30 (FIXED / CINEMATIC) */}
        <div className="flex-1 flex overflow-hidden w-full">

          {/* LEFT: Navigation Hub (10%) */}
          <div className="flex-[0_0_10%] h-full border-r border-white/5 bg-[#030712] override-nav-width">
            <NavigationPanel />
          </div>

          {/* CENTER: Active Canvas (60%) */}
          <div className="flex-[0_0_60%] h-full overflow-hidden bg-[#0a0a0f] relative border-r border-white/5">
            <WorkArea />
          </div>

          {/* RIGHT: PILI Intelligence (30%) */}
          <div className="flex-[0_0_30%] h-full bg-[#030712] border-l border-white/5 shadow-2xl z-20">
            <AnimatedAIChat />
          </div>

        </div>
      </div>
    </PiliProvider>
  )
}

export default App
