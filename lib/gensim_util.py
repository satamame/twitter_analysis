class StreamCorpus(object):
    def __init__(self, file_name):
        """
        コンストラクタ

        parameters
        ----------
        file_name : str
            コーパス用テキストファイルの名前
        """
        self.file_name = file_name
    
    def __iter__(self):
        """
        イテレータ
        """
        with open(self.file_name) as f:
            for l in f.readlines():
                yield eval(l)
