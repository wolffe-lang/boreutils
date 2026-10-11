# bu21: shared by the case generators.
import json
class Cases:
    def __init__(self):
        self.out = []
    def note(self, text):
        self.pending = "\n".join("# " + l for l in text.split("\n"))
    def case(self, name, args, **kw):
        lines = ["[[case]]", f"name = {json.dumps(name)}", "args = " + json.dumps(args)]
        if getattr(self, "pending", None):
            lines.insert(0, self.pending)
            self.pending = None
        for k, v in kw.items():
            if k == "umask":
                lines.append(f"umask = 0o{v:03o}")
            elif k == "scratch_modes":
                lines.append("scratch_modes = { " + ", ".join(f"{json.dumps(a)} = 0o{b:03o}" for a, b in v.items()) + " }")
            elif isinstance(v, dict):
                lines.append(f"{k} = {{ " + ", ".join(f"{json.dumps(a)} = {json.dumps(b)}" for a, b in v.items()) + " }")
            else:
                lines.append(f"{k} = {json.dumps(v)}")
        self.out.append("\n".join(lines))
    def write(self, path, head):
        import os, re
        util = os.path.basename(path)[:-5]
        field = json.load(open(os.path.join(os.path.dirname(__file__), "field.json"))).get(util, [])
        used = 0
        for k, c in enumerate(self.out):
            m = re.search(r'^name = (.*)$', c, re.M)
            if json.loads(m.group(1)) in field:
                self.out[k] = c + '\ngnu_min = "9.11"'
                used += 1
        assert used == len(field), (used, len(field))
        if field:
            head += ("#\n# A case that says gnu_min = \"9.11\" is one the field's GNU 9.4 answers\n"
                     "# differently (CI's `field` leg, run 38123623741): there it is skipped,\n"
                     "# which keeps that leg's list a record of the field and not of this file.\n")
        names = [l for c in self.out for l in c.split("\n") if l.startswith("name = ")]
        assert len(names) == len(set(names)), [n for n in names if names.count(n) > 1]
        open(path, "w").write(head + "\n" + "\n\n".join(self.out) + "\n")
        print(len(self.out), "cases")
