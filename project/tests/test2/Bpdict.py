class BpDict(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def memo(self):
        return self._memo

    @memo.setter
    def memo(self, value):
        self._memo = value

    @property
    def file_level(self):
        return self._file_level

    @file_level.setter
    def file_level(self, value):
        self._file_level = value

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, value):
        self._task_id = value

    @property
    def filesize(self):
        return self._filesize

    @filesize.setter
    def filesize(self, value):
        self._filesize = value

    @property
    def file_id(self):
        return self._file_id

    @file_id.setter
    def file_id(self, value):
        self._file_id = value

    @property
    def remote_path(self):
        return self._remote_path

    @remote_path.setter
    def remote_path(self, value):
        self._remote_path = value

    @property
    def send_state(self):
        return self._send_state

    @send_state.setter
    def send_state(self, value):
        self._send_state = value

    @property
    def share_type(self):
        return self._share_type

    @share_type.setter
    def share_type(self, value):
        self._share_type = value

    @property
    def ver_id(self):
        return self._ver_id

    @ver_id.setter
    def ver_id(self, value):
        self._ver_id = value

    @property
    def send_time(self):
        return self._send_time

    @send_time.setter
    def send_time(self, value):
        self._send_time = value

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, value):
        self._account = value

    @property
    def file_hash(self):
        return self._file_hash

    @file_hash.setter
    def file_hash(self, value):
        self._file_hash = value


a = BpDict()
