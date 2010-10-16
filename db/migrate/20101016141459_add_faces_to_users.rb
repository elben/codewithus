class AddFacesToUsers < ActiveRecord::Migration
  def self.up
    add_column :users, :face_url, :string
  end

  def self.down
    remove_column :users, :face_url
  end
end
