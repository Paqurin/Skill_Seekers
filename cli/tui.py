#!/usr/bin/env python3
"""
Skill Seeker TUI - Terminal User Interface with mouse support
Built with Textual framework for beautiful, interactive CLI experience
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Button, Static, DataTable, Tree, TabbedContent, TabPane, Input, Select, Label, ProgressBar, Log, DirectoryTree
from textual.binding import Binding
from textual.screen import Screen
from textual import events
from textual.reactive import reactive
from pathlib import Path
import json
import os
from datetime import datetime
from rich.text import Text


class DashboardScreen(Screen):
    """Main dashboard showing project overview"""

    BINDINGS = [
        ("c", "show_configs", "Configs"),
        ("s", "show_scrape", "Scrape"),
        ("k", "show_skills", "Skills"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="dashboard"):
            yield Static("🚀 Skill Seeker Dashboard", id="dashboard-title")

            # Quick Stats
            with Horizontal(id="stats-container"):
                yield Static(self.get_stat_card("📋 Configs", self.count_configs()), classes="stat-card")
                yield Static(self.get_stat_card("💾 Cached Data", self.count_cached()), classes="stat-card")
                yield Static(self.get_stat_card("📦 Built Skills", self.count_skills()), classes="stat-card")
                yield Static(self.get_stat_card("✅ Packaged", self.count_packages()), classes="stat-card")

            # Recent Activity
            with Vertical(id="activity-container"):
                yield Static("📊 Recent Activity", classes="section-title")
                yield Log(id="activity-log", auto_scroll=True)

            # Quick Actions
            with Vertical(id="quick-actions"):
                yield Static("⚡ Quick Actions", classes="section-title")
                with Horizontal(classes="action-buttons"):
                    yield Button("🎯 New Config", id="btn-new-config", variant="primary")
                    yield Button("🔍 Start Scrape", id="btn-start-scrape", variant="success")
                    yield Button("✨ Enhance Skill", id="btn-enhance", variant="warning")
                    yield Button("📤 Upload Skill", id="btn-upload", variant="error")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize dashboard data"""
        self.update_activity_log()

    def update_activity_log(self) -> None:
        """Update the activity log with recent events"""
        log = self.query_one("#activity-log", Log)
        log.clear()

        # Check for recent skills
        output_dir = Path("output")
        if output_dir.exists():
            skills = sorted(output_dir.glob("*/SKILL.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:5]
            for skill_file in skills:
                skill_name = skill_file.parent.name
                mod_time = datetime.fromtimestamp(skill_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                log.write_line(f"[green]✓[/green] Built skill: [bold]{skill_name}[/bold] ({mod_time})")

        if not log.lines:
            log.write_line("[dim]No recent activity[/dim]")

    def get_stat_card(self, title: str, count: int) -> str:
        """Generate a stat card"""
        return f"{title}\n[bold cyan]{count}[/bold cyan]"

    def count_configs(self) -> int:
        """Count available configs"""
        configs_dir = Path("configs")
        return len(list(configs_dir.glob("*.json"))) if configs_dir.exists() else 0

    def count_cached(self) -> int:
        """Count cached data directories"""
        output_dir = Path("output")
        return len(list(output_dir.glob("*_data"))) if output_dir.exists() else 0

    def count_skills(self) -> int:
        """Count built skills"""
        output_dir = Path("output")
        if not output_dir.exists():
            return 0
        skills = [d for d in output_dir.iterdir() if d.is_dir() and not d.name.endswith("_data") and (d / "SKILL.md").exists()]
        return len(skills)

    def count_packages(self) -> int:
        """Count packaged .zip files"""
        output_dir = Path("output")
        return len(list(output_dir.glob("*.zip"))) if output_dir.exists() else 0

    def action_show_configs(self) -> None:
        """Show configs screen"""
        self.app.push_screen(ConfigsScreen())

    def action_show_scrape(self) -> None:
        """Show scrape screen"""
        self.app.push_screen(ScrapeScreen())

    def action_show_skills(self) -> None:
        """Show skills screen"""
        self.app.push_screen(SkillsScreen())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "btn-new-config":
            self.app.push_screen(NewConfigScreen())
        elif event.button.id == "btn-start-scrape":
            self.app.push_screen(ScrapeScreen())
        elif event.button.id == "btn-enhance":
            self.app.push_screen(SkillsScreen())
        elif event.button.id == "btn-upload":
            self.app.push_screen(UploadScreen())


class ConfigsScreen(Screen):
    """Configuration browser and editor"""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("n", "new_config", "New"),
        ("v", "validate", "Validate"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="configs-container"):
            yield Static("📋 Configuration Manager", classes="screen-title")

            with Horizontal(id="configs-layout"):
                # Config list
                with Vertical(id="config-list", classes="panel"):
                    yield Static("Available Configs", classes="panel-title")
                    table = DataTable(id="configs-table")
                    table.cursor_type = "row"
                    yield table

                    with Horizontal(classes="action-buttons"):
                        yield Button("📝 New", id="btn-new-config", variant="primary")
                        yield Button("✓ Validate", id="btn-validate-config", variant="success")
                        yield Button("✂️ Split", id="btn-split-config")

                # Config preview
                with Vertical(id="config-preview", classes="panel"):
                    yield Static("Config Preview", classes="panel-title")
                    yield Log(id="config-content", auto_scroll=False)

        yield Footer()

    def on_mount(self) -> None:
        """Initialize configs table"""
        table = self.query_one("#configs-table", DataTable)
        table.add_columns("Name", "URL", "Max Pages", "Categories")

        # Load configs
        configs_dir = Path("configs")
        if configs_dir.exists():
            for config_file in sorted(configs_dir.glob("*.json")):
                try:
                    with open(config_file) as f:
                        config = json.load(f)

                    name = config.get("name", config_file.stem)
                    url = config.get("base_url", "")[:40] + "..." if len(config.get("base_url", "")) > 40 else config.get("base_url", "")
                    max_pages = str(config.get("max_pages", "N/A"))
                    categories = str(len(config.get("categories", {})))

                    table.add_row(name, url, max_pages, categories, key=str(config_file))
                except Exception as e:
                    table.add_row(config_file.stem, f"Error: {e}", "", "", key=str(config_file))

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Show config preview when row selected"""
        config_file = Path(event.row_key.value)
        log = self.query_one("#config-content", Log)
        log.clear()

        try:
            with open(config_file) as f:
                config = json.load(f)

            log.write_line(f"[bold cyan]File:[/bold cyan] {config_file.name}")
            log.write_line(f"[bold cyan]Name:[/bold cyan] {config.get('name', 'N/A')}")
            log.write_line(f"[bold cyan]Description:[/bold cyan] {config.get('description', 'N/A')}")
            log.write_line(f"[bold cyan]Base URL:[/bold cyan] {config.get('base_url', 'N/A')}")
            log.write_line(f"[bold cyan]Max Pages:[/bold cyan] {config.get('max_pages', 'N/A')}")
            log.write_line(f"[bold cyan]Rate Limit:[/bold cyan] {config.get('rate_limit', 'N/A')}s")
            log.write_line("")
            log.write_line("[bold cyan]Categories:[/bold cyan]")
            for cat, keywords in config.get("categories", {}).items():
                log.write_line(f"  • {cat}: {', '.join(keywords[:3])}...")
        except Exception as e:
            log.write_line(f"[red]Error loading config: {e}[/red]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "btn-new-config":
            self.app.push_screen(NewConfigScreen())
        elif event.button.id == "btn-validate-config":
            # Validate selected config
            table = self.query_one("#configs-table", DataTable)
            if table.cursor_row is not None:
                self.notify("✓ Config validation feature coming soon!")
        elif event.button.id == "btn-split-config":
            self.notify("✂️ Config splitting feature coming soon!")


class NewConfigScreen(Screen):
    """Create a new configuration"""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="new-config-container"):
            yield Static("📝 Create New Configuration", classes="screen-title")

            with Vertical(id="config-form", classes="form"):
                yield Label("Skill Name:")
                yield Input(placeholder="e.g., react, vue, godot", id="input-name")

                yield Label("Documentation URL:")
                yield Input(placeholder="https://docs.example.com/", id="input-url")

                yield Label("Description:")
                yield Input(placeholder="When to use this skill", id="input-description")

                yield Label("Max Pages:")
                yield Input(placeholder="100", id="input-max-pages", value="100")

                with Horizontal(classes="action-buttons"):
                    yield Button("✓ Create", id="btn-create", variant="success")
                    yield Button("✗ Cancel", id="btn-cancel")

                yield Static("", id="form-status")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle form submission"""
        if event.button.id == "btn-create":
            # Get form values
            name = self.query_one("#input-name", Input).value
            url = self.query_one("#input-url", Input).value
            description = self.query_one("#input-description", Input).value
            max_pages = self.query_one("#input-max-pages", Input).value

            # Validate
            if not name or not url:
                self.query_one("#form-status", Static).update("[red]Name and URL are required[/red]")
                return

            # Create config
            try:
                config = {
                    "name": name,
                    "description": description,
                    "base_url": url,
                    "selectors": {
                        "main_content": "article",
                        "title": "title",
                        "code_blocks": "pre"
                    },
                    "url_patterns": {
                        "include": [],
                        "exclude": ["/search", "/_static/"]
                    },
                    "categories": {},
                    "rate_limit": 0.5,
                    "max_pages": int(max_pages) if max_pages else 100
                }

                config_file = Path("configs") / f"{name}.json"
                config_file.parent.mkdir(exist_ok=True)

                with open(config_file, "w") as f:
                    json.dump(config, f, indent=2)

                self.notify(f"✓ Created {config_file.name}")
                self.app.pop_screen()
            except Exception as e:
                self.query_one("#form-status", Static).update(f"[red]Error: {e}[/red]")

        elif event.button.id == "btn-cancel":
            self.app.pop_screen()


class ScrapeScreen(Screen):
    """Scraping workflow with progress"""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="scrape-container"):
            yield Static("🔍 Documentation Scraper", classes="screen-title")

            with TabbedContent(id="scrape-tabs"):
                # Tab 1: Use existing config
                with TabPane("📋 From Config", id="tab-config"):
                    with Vertical(id="scrape-form-config"):
                        yield Label("Select Configuration:")
                        yield Select(
                            options=[(cfg.stem, cfg.stem) for cfg in Path("configs").glob("*.json")] if Path("configs").exists() else [],
                            id="select-config"
                        )

                        yield Label("Options:")
                        with Horizontal(classes="checkbox-group"):
                            yield Button("☐ Skip Scrape (use cache)", id="btn-skip-scrape", classes="checkbox-btn")
                            yield Button("☐ Resume from checkpoint", id="btn-resume", classes="checkbox-btn")
                            yield Button("☐ Fresh start", id="btn-fresh", classes="checkbox-btn")

                        yield Label("Max Pages Override (optional):")
                        yield Input(placeholder="Leave empty to use config value", id="input-override-pages")

                        with Horizontal(classes="action-buttons"):
                            yield Button("🚀 Start Scrape", id="btn-start-scrape", variant="primary")
                            yield Button("📊 Estimate Only", id="btn-estimate", variant="success")

                # Tab 2: Quick scrape from URL
                with TabPane("🌐 Quick Scrape", id="tab-quick"):
                    with Vertical(id="scrape-form-quick", classes="form"):
                        yield Label("Skill Name:")
                        yield Input(placeholder="e.g., react, vue, my-docs", id="input-quick-name")

                        yield Label("Documentation URL:")
                        yield Input(placeholder="https://docs.example.com/", id="input-quick-url")

                        yield Label("Description:")
                        yield Input(placeholder="When to use this skill", id="input-quick-description")

                        yield Label("Max Pages:")
                        yield Input(placeholder="100", id="input-quick-max-pages", value="100")

                        yield Label("Main Content Selector (CSS):")
                        yield Input(placeholder="article, main, div[role='main']", id="input-quick-selector", value="article")

                        with Horizontal(classes="action-buttons"):
                            yield Button("🚀 Scrape Now", id="btn-quick-scrape", variant="primary")
                            yield Button("💾 Save as Config", id="btn-save-config", variant="success")

                        yield Static("", id="quick-status")

            # Shared output area
            with Vertical(id="scrape-output"):
                yield Static("", id="scrape-status")
                yield ProgressBar(id="scrape-progress", show_eta=False)
                yield Log(id="scrape-log", auto_scroll=True)

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle scraping actions"""
        if event.button.id == "btn-start-scrape":
            self.notify("🚀 Scraping will be integrated with doc_scraper.py")
        elif event.button.id == "btn-estimate":
            self.notify("📊 Estimation will be integrated with estimate_pages.py")
        elif event.button.id == "btn-quick-scrape":
            self.handle_quick_scrape()
        elif event.button.id == "btn-save-config":
            self.handle_save_config()
        elif event.button.id in ["btn-skip-scrape", "btn-resume", "btn-fresh"]:
            # Toggle checkbox buttons
            button = event.button
            label_text = str(button.label)
            if "☐" in label_text:
                button.label = label_text.replace("☐", "☑")
            else:
                button.label = label_text.replace("☑", "☐")

    def handle_quick_scrape(self) -> None:
        """Handle quick scrape from URL"""
        # Get form values
        name = self.query_one("#input-quick-name", Input).value
        url = self.query_one("#input-quick-url", Input).value
        description = self.query_one("#input-quick-description", Input).value
        max_pages = self.query_one("#input-quick-max-pages", Input).value
        selector = self.query_one("#input-quick-selector", Input).value

        # Validate
        status = self.query_one("#quick-status", Static)
        if not name or not url:
            status.update("[red]❌ Name and URL are required[/red]")
            return

        # Show progress
        log = self.query_one("#scrape-log", Log)
        log.clear()
        log.write_line(f"[cyan]Starting quick scrape:[/cyan]")
        log.write_line(f"  Name: {name}")
        log.write_line(f"  URL: {url}")
        log.write_line(f"  Max Pages: {max_pages or 'default'}")
        log.write_line(f"  Selector: {selector}")
        log.write_line("")

        # Create temporary config
        config = {
            "name": name,
            "description": description or f"Documentation for {name}",
            "base_url": url,
            "selectors": {
                "main_content": selector or "article",
                "title": "title",
                "code_blocks": "pre"
            },
            "url_patterns": {
                "include": [],
                "exclude": ["/search", "/_static/"]
            },
            "categories": {},
            "rate_limit": 0.5,
            "max_pages": int(max_pages) if max_pages else 100
        }

        # TODO: Integrate with actual scraping logic
        log.write_line("[yellow]⚠ Quick scrape will be integrated with doc_scraper.py[/yellow]")
        log.write_line(f"[green]✓[/green] Config created temporarily")
        log.write_line(f"[yellow]→[/yellow] Would scrape from: {url}")
        log.write_line(f"[yellow]→[/yellow] Would save to: output/{name}/")

        status.update("[green]✓ Ready to scrape! (Integration pending)[/green]")
        self.notify(f"🚀 Quick scrape configured for {name}")

    def handle_save_config(self) -> None:
        """Save quick scrape form as a permanent config file"""
        # Get form values
        name = self.query_one("#input-quick-name", Input).value
        url = self.query_one("#input-quick-url", Input).value
        description = self.query_one("#input-quick-description", Input).value
        max_pages = self.query_one("#input-quick-max-pages", Input).value
        selector = self.query_one("#input-quick-selector", Input).value

        # Validate
        status = self.query_one("#quick-status", Static)
        if not name or not url:
            status.update("[red]❌ Name and URL are required[/red]")
            return

        # Create config
        try:
            config = {
                "name": name,
                "description": description or f"Documentation for {name}",
                "base_url": url,
                "selectors": {
                    "main_content": selector or "article",
                    "title": "title",
                    "code_blocks": "pre"
                },
                "url_patterns": {
                    "include": [],
                    "exclude": ["/search", "/_static/"]
                },
                "categories": {},
                "rate_limit": 0.5,
                "max_pages": int(max_pages) if max_pages else 100
            }

            config_file = Path("configs") / f"{name}.json"
            config_file.parent.mkdir(exist_ok=True)

            with open(config_file, "w") as f:
                json.dump(config, f, indent=2)

            status.update(f"[green]✓ Saved to {config_file.name}[/green]")
            self.notify(f"💾 Config saved: {config_file.name}")

            # Refresh config dropdown in other tab
            select = self.query_one("#select-config", Select)
            select.set_options([(cfg.stem, cfg.stem) for cfg in Path("configs").glob("*.json")])

        except Exception as e:
            status.update(f"[red]❌ Error: {e}[/red]")


class SkillsScreen(Screen):
    """Skill management - enhance, package, upload"""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="skills-container"):
            yield Static("📦 Skill Manager", classes="screen-title")

            with Horizontal(id="skills-layout"):
                # Skill list
                with Vertical(id="skill-list", classes="panel"):
                    yield Static("Built Skills", classes="panel-title")
                    table = DataTable(id="skills-table")
                    table.cursor_type = "row"
                    yield table

                # Skill actions
                with Vertical(id="skill-actions", classes="panel"):
                    yield Static("Actions", classes="panel-title")
                    yield Button("✨ Enhance (Local)", id="btn-enhance-local", variant="primary")
                    yield Button("✨ Enhance (API)", id="btn-enhance-api")
                    yield Button("📦 Package", id="btn-package", variant="success")
                    yield Button("📤 Upload to Claude", id="btn-upload", variant="warning")
                    yield Button("🗑️ Delete", id="btn-delete", variant="error")

                    yield Static("", id="skill-info")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize skills table"""
        table = self.query_one("#skills-table", DataTable)
        table.add_columns("Skill Name", "Size", "Modified", "Status")

        # Load skills
        output_dir = Path("output")
        if output_dir.exists():
            skills = [d for d in output_dir.iterdir() if d.is_dir() and not d.name.endswith("_data")]
            for skill_dir in sorted(skills):
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    stat = skill_file.stat()
                    size = f"{stat.st_size // 1024}KB"
                    modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")

                    # Check status
                    has_backup = (skill_dir / "SKILL.md.backup").exists()
                    is_packaged = (output_dir / f"{skill_dir.name}.zip").exists()

                    status = []
                    if has_backup:
                        status.append("✨")
                    if is_packaged:
                        status.append("📦")

                    table.add_row(skill_dir.name, size, modified, " ".join(status) or "-", key=str(skill_dir))

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Show skill info when selected"""
        skill_dir = Path(event.row_key.value)
        info = self.query_one("#skill-info", Static)

        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            with open(skill_file) as f:
                lines = f.readlines()[:5]  # First 5 lines

            preview = "".join(lines)
            info.update(f"[bold]{skill_dir.name}[/bold]\n\n{preview}...")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle skill actions"""
        table = self.query_one("#skills-table", DataTable)
        if table.cursor_row is None:
            self.notify("⚠️ Please select a skill first")
            return

        skill_dir = Path(list(table.rows.keys())[table.cursor_row])

        if event.button.id == "btn-enhance-local":
            self.notify(f"✨ Will enhance {skill_dir.name} with LOCAL mode")
        elif event.button.id == "btn-enhance-api":
            self.notify(f"✨ Will enhance {skill_dir.name} with API mode")
        elif event.button.id == "btn-package":
            self.notify(f"📦 Will package {skill_dir.name}")
        elif event.button.id == "btn-upload":
            self.notify(f"📤 Will upload {skill_dir.name}")
        elif event.button.id == "btn-delete":
            self.notify(f"🗑️ Delete confirmation coming soon for {skill_dir.name}")


class UploadScreen(Screen):
    """Upload packaged skills to Claude"""

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="upload-container"):
            yield Static("📤 Upload to Claude", classes="screen-title")

            with Vertical(id="upload-form"):
                yield Label("Select Package:")
                yield Select(
                    options=[(p.name, str(p)) for p in Path("output").glob("*.zip")] if Path("output").exists() else [],
                    id="select-package"
                )

                yield Label("API Key Status:")
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if api_key:
                    yield Static(f"[green]✓[/green] API Key found: {api_key[:20]}...")
                else:
                    yield Static("[yellow]⚠[/yellow] No API key found (set ANTHROPIC_API_KEY)")

                with Horizontal(classes="action-buttons"):
                    yield Button("📤 Upload", id="btn-upload-now", variant="primary")
                    yield Button("📋 Batch Upload", id="btn-batch-upload", variant="success")

                yield Log(id="upload-log", auto_scroll=True)

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle upload actions"""
        if event.button.id == "btn-upload-now":
            self.notify("📤 Upload will be integrated with upload_skill.py")
        elif event.button.id == "btn-batch-upload":
            self.notify("📋 Batch upload feature coming soon!")


class SkillSeekerTUI(App):
    """Skill Seeker Terminal User Interface"""

    CSS = """
    Screen {
        background: $surface;
    }

    #dashboard {
        width: 100%;
        height: 100%;
        padding: 1 2;
    }

    #dashboard-title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
        content-align: center middle;
    }

    #stats-container {
        height: 5;
        margin-bottom: 1;
    }

    .stat-card {
        border: solid $primary;
        width: 1fr;
        height: 100%;
        padding: 1 2;
        text-align: center;
        content-align: center middle;
    }

    #activity-container {
        height: 1fr;
        border: solid $success;
        padding: 1 2;
        margin-bottom: 1;
    }

    #quick-actions {
        height: 6;
        border: solid $warning;
        padding: 1 2;
    }

    .section-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    .action-buttons {
        height: 3;
        align: center middle;
    }

    Button {
        margin: 0 1;
    }

    .screen-title {
        text-align: center;
        text-style: bold;
        color: $accent;
        padding: 1;
        content-align: center middle;
    }

    .panel {
        border: solid $primary;
        padding: 1;
        width: 1fr;
    }

    .panel-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    #configs-layout {
        height: 1fr;
    }

    #config-list {
        width: 60%;
    }

    #config-preview {
        width: 40%;
    }

    #skills-layout {
        height: 1fr;
    }

    #skill-list {
        width: 70%;
    }

    #skill-actions {
        width: 30%;
    }

    .form {
        width: 60;
        margin: 2 4;
        padding: 2;
        border: solid $primary;
    }

    Input {
        margin-bottom: 1;
    }

    Label {
        margin-top: 1;
        text-style: bold;
        color: $text;
    }

    .checkbox-btn {
        width: auto;
    }

    DataTable {
        height: 1fr;
        margin-bottom: 1;
    }

    Log {
        height: 1fr;
        border: solid $primary-darken-1;
        background: $panel;
    }

    ProgressBar {
        margin: 1 0;
    }
    """

    TITLE = "Skill Seeker TUI"
    SUB_TITLE = "Convert documentation to Claude AI skills"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "show_dashboard", "Dashboard"),
    ]

    def on_mount(self) -> None:
        """Show dashboard on startup"""
        self.push_screen(DashboardScreen())

    def action_show_dashboard(self) -> None:
        """Return to dashboard"""
        self.pop_screen()
        self.push_screen(DashboardScreen())


def run_tui():
    """Entry point for TUI"""
    app = SkillSeekerTUI()
    app.run()


if __name__ == "__main__":
    run_tui()
