class CreatePulls < ActiveRecord::Migration
  def self.up
    create_table :pulls do |t|
      t.string :active_branch

      t.timestamps
    end
  end

  def self.down
    drop_table :pulls
  end
end
