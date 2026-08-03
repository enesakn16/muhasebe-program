import ast
import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "demo" / "demo_app.py"
SPEC = importlib.util.spec_from_file_location("demo_app", MODULE_PATH)
DEMO = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(DEMO)


class DemoModeTests(unittest.TestCase):
    def test_store_uses_in_memory_database(self):
        store = DEMO.DemoStore()
        try:
            databases = store.connection.execute("PRAGMA database_list").fetchall()
            self.assertEqual(databases[0][2], "")
        finally:
            store.close()

    def test_seed_data_is_fictional_and_summary_is_deterministic(self):
        store = DEMO.DemoStore()
        try:
            names = [row["name"] for row in store.accounts()]
            self.assertTrue(all("Demo" in name or "Örnek" in name for name in names))
            summary = store.summary()
            self.assertEqual(summary.receivable, 26170.50)
            self.assertEqual(summary.payable, 17250.00)
            self.assertEqual(summary.overdue, 12370.50)
        finally:
            store.close()

    def test_demo_module_has_no_network_or_environment_imports(self):
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        imported_roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])

        forbidden = {"requests", "httpx", "urllib", "socket", "supabase", "dotenv", "os"}
        self.assertTrue(imported_roots.isdisjoint(forbidden))


if __name__ == "__main__":
    unittest.main()
