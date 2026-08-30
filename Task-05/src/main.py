import curses

import psutil as ps


def main(stdscr):
    # Calculates number of rows to display
    height, _ = stdscr.getmaxyx()
    size = height - 3
    
    offset = 0

    stdscr.nodelay(True)
    stdscr.keypad(True)

    while True:
        count = len(ps.pids())
        visible = ps.pids()[offset : offset + size]

        stdscr.erase()

        # Initial headings
        stdscr.addstr(0, 0, "PID")
        stdscr.addstr(0, 8, "Process Name")
        stdscr.addstr(0, 48, "Memory Usage")
        stdscr.addstr(0, 63, "CPU Usage")

        for i, pid in enumerate(visible):
            proc = ps.Process(pid)
            stdscr.addstr(1 + i, 0, str(pid))
            stdscr.addstr(1 + i, 8, proc.name())
            stdscr.addstr(1 + i, 48, f"{proc.memory_percent():.2f}%")
            stdscr.addstr(1 + i, 63, f"{proc.cpu_percent():.2f}%")

        stdscr.addstr(35, 0, "-" * 72)
        stdscr.addstr(36, 0, f"Total process count: {count}")

        stdscr.timeout(50)

        # Keyboard controls
        key = stdscr.getch()
        if key == ord("q"):
            break
        elif key == curses.KEY_UP:
            offset -= 1
            offset = max(offset, 0)
        elif key == curses.KEY_DOWN:
            offset += 1
            offset = min(offset, count - size)

        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
