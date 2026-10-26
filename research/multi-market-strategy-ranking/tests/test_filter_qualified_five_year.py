import csv
import gzip
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from filter_qualified_five_year import qualify, run

class QualificationTests(unittest.TestCase):
    def row(self, ret, trades, kelly, dd="10"):
        return {"五年收益_pct": str(ret), "五年交易數": str(trades),
                "IS_Kelly_pct": str(kelly), "五年最大回撤_pct": str(dd),
                "策略": "test"}

    def test_strict_thresholds_and_invalid_values(self):
        rows = [self.row(101,70,1), self.row(100,70,1),
                self.row(101,69,1), self.row(101,70,0),
                self.row("nan",100,2), self.row(150,"70.5",3),
                self.row(102,75,4)]
        total, selected = qualify(rows)
        self.assertEqual(total, 7)
        self.assertEqual([r["五年收益_pct"] for r in selected], ["102", "101"])

    def test_gzip_input_and_output_preserves_original(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp)/"original.csv.gz"
            out = Path(tmp)/"qualified.csv"
            with gzip.open(inp,"wt",encoding="utf-8",newline="") as stream:
                writer=csv.DictWriter(stream,fieldnames=list(self.row(1,1,1)))
                writer.writeheader()
                writer.writerows([self.row(120,75,10),self.row(110,2,20)])
            before=inp.read_bytes()
            self.assertEqual(run(inp,out),(2,1))
            self.assertEqual(inp.read_bytes(),before)
            with out.open(encoding="utf-8-sig",newline="") as stream:
                self.assertEqual(len(list(csv.DictReader(stream))),1)

    def test_missing_required_column_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp=Path(tmp)/"bad.csv"
            inp.write_text("五年收益_pct,五年交易數\n101,75\n",encoding="utf-8")
            with self.assertRaises(ValueError):
                run(inp,Path(tmp)/"output.csv")

if __name__ == "__main__":
    unittest.main()
