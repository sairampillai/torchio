import unittest
import tempfile
from pathlib import Path

from torch.utils.data import DataLoader
from torchio.data import ImageSampler
from torchio import ImagesDataset, Queue, DATA
from torchio.utils import create_dummy_dataset


class TestQueue(unittest.TestCase):
    """Tests for `queue` module."""
    def setUp(self):
        """Set up test fixtures, if any."""
        self.dir = Path(tempfile.gettempdir()) / 'torchio'
        self.subjects_list = create_dummy_dataset(
            num_images=10,
            size_range=(10, 20),
            directory=self.dir,
            suffix='.nii',
            force=False,
        )

    def tearDown(self):
        """Tear down test fixtures, if any."""
        import shutil
        shutil.rmtree(self.dir)

    def test_queue(self):
        subjects_dataset = ImagesDataset(self.subjects_list)
        queue_dataset = Queue(
            subjects_dataset,
            max_length=6,
            samples_per_volume=2,
            patch_size=10,
            sampler_class=ImageSampler,
            num_workers=2,
            verbose=True,
        )
        _ = str(queue_dataset)
        batch_loader = DataLoader(queue_dataset, batch_size=4)
        for batch in batch_loader:
            _ = batch['one_modality'][DATA]
            _ = batch['segmentation'][DATA]
