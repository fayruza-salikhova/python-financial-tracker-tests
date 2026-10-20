class TestTransactions:
    def test_add_transaction(self, tracker):
        tracker.add_transaction("2020-01-01", amount=50)
        tracker.add_transaction("2020-01-01", amount=-1000)
        assert len(tracker.list_transactions()) == 2

    def test_delete_transactions(self, tracker):
        tx1 = tracker.add_transaction("2020-01-01", amount=50)
        tx2 = tracker.add_transaction("2020-01-01", amount=-1000)
        tracker.delete_transaction(tx1)

        assert len(tracker.list_transactions()) == 1
        assert tracker.list_transactions()[0].id == tx2
